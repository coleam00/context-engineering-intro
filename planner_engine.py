"""
Core planning engine for Modulblok Inspection Planning System.

Handles:
- Order matching with customer master data
- Geocoding addresses
- Geographic clustering
- TSP route optimization
- Inspector assignment
- Daily scheduling
- Planning generation
"""

import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from sklearn.cluster import KMeans

from config import (
    GEOCODING,
    INSPECTORS,
    PAOLO_REGIONS,
    NATIONAL_INSPECTORS,
    REGIONAL_COORDS,
    WORK_PARAMS,
    validate_inspector_assignment,
    get_available_inspectors,
)
from utils import (
    normalize_string,
    calculate_distance,
    calculate_travel_time,
    is_available,
    next_available_date,
    get_week_number,
    get_day_name_italian,
)


# ============================================================================
# ORDER MATCHING
# ============================================================================


def match_orders(
    anagrafica_df: pd.DataFrame, ordini_df: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Match orders with customer master data.

    Performs inner join on normalized (Cliente, Indirizzo).
    Only matched orders proceed to planning.

    Args:
        anagrafica_df: Customer master data
        ordini_df: Confirmed orders

    Returns:
        Tuple of (matched DataFrame, unmatched orders DataFrame)

    Example:
        >>> matched, unmatched = match_orders(anagrafica_df, ordini_df)
        >>> print(f"Matched: {len(matched)}, Unmatched: {len(unmatched)}")
    """
    # Create normalized columns for matching
    anagrafica_df["cliente_norm"] = anagrafica_df["Nome del Cliente"].apply(
        normalize_string
    )
    anagrafica_df["indirizzo_norm"] = anagrafica_df["Indirizzo completo"].apply(
        normalize_string
    )

    ordini_df["cliente_norm"] = ordini_df["Cliente"].apply(normalize_string)
    ordini_df["indirizzo_norm"] = ordini_df["Indirizzo_Sede"].apply(normalize_string)

    # Inner join on normalized columns
    matched = ordini_df.merge(
        anagrafica_df,
        on=["cliente_norm", "indirizzo_norm"],
        how="inner",
        suffixes=("_ordine", "_anagrafica"),
    )

    # Find unmatched orders
    matched_order_ids = matched["ID_Ordine"].unique()
    unmatched = ordini_df[~ordini_df["ID_Ordine"].isin(matched_order_ids)]

    # Clean up temporary columns
    matched = matched.drop(columns=["cliente_norm", "indirizzo_norm"])
    unmatched = unmatched.drop(columns=["cliente_norm", "indirizzo_norm"])

    return matched, unmatched


# ============================================================================
# GEOCODING
# ============================================================================


def geocode_addresses(
    df: pd.DataFrame, progress_callback=None
) -> pd.DataFrame:
    """
    Geocode addresses to get latitude/longitude coordinates.

    Uses Nominatim (OpenStreetMap) with rate limiting.
    Falls back to regional coordinates if geocoding fails.

    Args:
        df: DataFrame with CAP, Città, Regione columns
        progress_callback: Optional callback function(current, total, message)

    Returns:
        DataFrame with added 'lat' and 'lon' columns

    Example:
        >>> df = geocode_addresses(df, lambda i, n, msg: print(f"{i}/{n}: {msg}"))
    """
    # Initialize geolocator
    geolocator = Nominatim(
        user_agent=GEOCODING["user_agent"], timeout=GEOCODING["timeout"]
    )

    # Add columns
    df["lat"] = 0.0
    df["lon"] = 0.0

    total = len(df)

    for idx, row in df.iterrows():
        # Progress callback
        if progress_callback:
            progress_callback(
                idx + 1,
                total,
                f"Geocodifica {row['Città']} ({idx + 1}/{total})",
            )

        try:
            # Try geocoding with CAP + Città
            query = f"{row['CAP']} {row['Città']}, {GEOCODING['country']}"
            location = geolocator.geocode(query)

            if location:
                df.at[idx, "lat"] = location.latitude
                df.at[idx, "lon"] = location.longitude
            else:
                # Fallback to regional coordinates
                region = row["Regione"]
                if region in REGIONAL_COORDS:
                    coords = REGIONAL_COORDS[region]
                    df.at[idx, "lat"] = coords[0]
                    df.at[idx, "lon"] = coords[1]

        except Exception as e:
            print(f"Errore geocoding per {row['Città']}: {e}")
            # Fallback to regional coordinates
            region = row["Regione"]
            if region in REGIONAL_COORDS:
                coords = REGIONAL_COORDS[region]
                df.at[idx, "lat"] = coords[0]
                df.at[idx, "lon"] = coords[1]

        # Rate limiting (Nominatim requires 1 req/sec)
        time.sleep(GEOCODING["rate_limit"])

    return df


# ============================================================================
# GEOGRAPHIC CLUSTERING
# ============================================================================


def cluster_geographic(
    df: pd.DataFrame, n_clusters: int = None
) -> pd.DataFrame:
    """
    Cluster customers by geographic location using K-means.

    Args:
        df: DataFrame with 'lat' and 'lon' columns
        n_clusters: Number of clusters (default from config)

    Returns:
        DataFrame with added 'cluster_id' column

    Example:
        >>> df = cluster_geographic(df, n_clusters=8)
    """
    if n_clusters is None:
        n_clusters = WORK_PARAMS["default_clusters"]

    # Adjust clusters if fewer clients
    n_clusters = min(n_clusters, len(df))

    if n_clusters < 1:
        df["cluster_id"] = 0
        return df

    # Extract coordinates
    coords = df[["lat", "lon"]].values

    # K-means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df["cluster_id"] = kmeans.fit_predict(coords)

    return df


# ============================================================================
# TSP OPTIMIZATION (Nearest Neighbor Heuristic)
# ============================================================================


def tsp_nearest_neighbor(
    clients_df: pd.DataFrame, base_coords: Tuple[float, float]
) -> pd.DataFrame:
    """
    Optimize tour using nearest neighbor algorithm (greedy TSP heuristic).

    Algorithm:
    1. Start with client closest to base
    2. Always visit the nearest unvisited client next
    3. Return ordered list

    Args:
        clients_df: DataFrame with 'lat', 'lon' columns
        base_coords: (latitude, longitude) of base location

    Returns:
        DataFrame sorted in optimal tour order with 'km_from_previous' column

    Example:
        >>> optimized = tsp_nearest_neighbor(clients_df, (46.08, 13.18))
    """
    if len(clients_df) == 0:
        return clients_df

    # Make a copy to avoid modifying original
    unvisited = clients_df.copy().reset_index(drop=True)
    tour = []
    current_coords = base_coords
    total_km = 0.0

    while len(unvisited) > 0:
        # Calculate distances from current position to all unvisited clients
        distances = []
        for idx, row in unvisited.iterrows():
            client_coords = (row["lat"], row["lon"])
            dist = calculate_distance(current_coords, client_coords)
            distances.append((idx, dist))

        # Find nearest client
        nearest_idx, distance = min(distances, key=lambda x: x[1])
        nearest_client = unvisited.loc[nearest_idx].copy()

        # Add distance to this client
        nearest_client["km_from_previous"] = distance
        total_km += distance

        # Add to tour
        tour.append(nearest_client)

        # Update current position
        current_coords = (nearest_client["lat"], nearest_client["lon"])

        # Remove from unvisited
        unvisited = unvisited.drop(nearest_idx).reset_index(drop=True)

    # Convert tour to DataFrame
    tour_df = pd.DataFrame(tour).reset_index(drop=True)

    return tour_df


# ============================================================================
# INSPECTOR ASSIGNMENT
# ============================================================================


def assign_inspectors(df: pd.DataFrame) -> pd.DataFrame:
    """
    Assign inspectors to visits respecting Paolo's regional constraint.

    Rules:
    - Paolo ONLY for: Lombardia, Piemonte, Liguria, Valle d'Aosta
    - Others: Random assignment among Adrian, Salvatore, Mattia

    Args:
        df: DataFrame with 'Regione' column

    Returns:
        DataFrame with added 'Ispettore' column

    Example:
        >>> df = assign_inspectors(df)
    """
    import random

    inspectors = []

    for _, row in df.iterrows():
        region = row["Regione"]

        # Get available inspectors for this region
        available = get_available_inspectors(region)

        # Assign inspector
        if len(available) == 1:
            # Paolo's regions - only Paolo can go
            inspector = available[0]
        else:
            # National regions - random assignment
            inspector = random.choice(available)

        inspectors.append(inspector)

    df["Ispettore"] = inspectors

    return df


# ============================================================================
# DAILY SCHEDULING
# ============================================================================


def schedule_daily(
    clients_df: pd.DataFrame,
    inspector: str,
    start_date: datetime = None,
    vacations_df: pd.DataFrame = None,
) -> pd.DataFrame:
    """
    Assign dates to visits respecting daily constraints.

    Constraints:
    - Max 8 hours/day (including travel time)
    - No weekends
    - No holidays
    - Buffer time per visit (+0.5h)
    - Friday return by 17:30 (max 6.5h)

    Args:
        clients_df: DataFrame with visits (pre-sorted by TSP)
        inspector: Inspector name
        start_date: Starting date (default: today)
        vacations_df: Vacation data for availability checks

    Returns:
        DataFrame with added 'Data', 'Settimana', 'Giorno' columns

    Example:
        >>> scheduled = schedule_daily(tour_df, "Adrian")
    """
    if start_date is None:
        start_date = datetime.now()

    # Ensure we start on a working day
    current_date = next_available_date(start_date, inspector, vacations_df)

    daily_hours = 0.0
    scheduled_visits = []

    for _, client in clients_df.iterrows():
        # Calculate hours needed for this visit
        visit_hours = client["Ore lavoro"] + WORK_PARAMS["buffer_hours_per_visit"]
        travel_hours = calculate_travel_time(client["km_from_previous"])
        total_hours = visit_hours + travel_hours

        # Check if it's Friday (stricter limit)
        is_friday = current_date.weekday() == 4
        max_daily_hours = (
            WORK_PARAMS["max_hours_friday"]
            if is_friday
            else WORK_PARAMS["max_hours_per_day"]
        )

        # Check if visit fits in current day
        if daily_hours + total_hours > max_daily_hours:
            # Move to next available day
            current_date = next_available_date(
                current_date + timedelta(days=1), inspector, vacations_df
            )
            daily_hours = 0.0

        # Assign to current date
        client_with_date = client.copy()
        client_with_date["Data"] = current_date
        client_with_date["Settimana"] = get_week_number(current_date)
        client_with_date["Giorno"] = get_day_name_italian(current_date)
        client_with_date["Ore_Totali_Giorno"] = daily_hours + total_hours

        scheduled_visits.append(client_with_date)

        # Update daily hours
        daily_hours += total_hours

    return pd.DataFrame(scheduled_visits)


# ============================================================================
# TOUR GENERATION
# ============================================================================


def generate_tours(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate optimized tours for all inspectors.

    Process:
    1. Group by cluster_id and Ispettore
    2. For each group, run TSP optimization
    3. Schedule visits day by day
    4. Combine all tours

    Args:
        df: DataFrame with matched and geocoded clients

    Returns:
        Complete planning DataFrame

    Example:
        >>> planning = generate_tours(matched_df)
    """
    all_tours = []

    # Group by inspector and cluster
    for (inspector, cluster), group in df.groupby(["Ispettore", "cluster_id"]):
        # Get base coordinates for this inspector
        base_coords = INSPECTORS[inspector]["base_coords"]

        # Run TSP optimization
        optimized_tour = tsp_nearest_neighbor(group, base_coords)

        # Schedule daily
        scheduled_tour = schedule_daily(optimized_tour, inspector)

        # Add tour zone name
        scheduled_tour["Tour_Zona"] = f"Cluster_{cluster}_{inspector}"

        all_tours.append(scheduled_tour)

    # Combine all tours
    if len(all_tours) == 0:
        return pd.DataFrame()

    complete_planning = pd.concat(all_tours, ignore_index=True)

    # Sort by inspector and date
    complete_planning = complete_planning.sort_values(
        ["Ispettore", "Data", "Settimana"]
    )

    return complete_planning


# ============================================================================
# RENEWALS LIST GENERATION
# ============================================================================


def generate_renewals_list(
    anagrafica_df: pd.DataFrame, alert_days: int = None
) -> pd.DataFrame:
    """
    Generate list of customers with contracts expiring soon.

    Args:
        anagrafica_df: Customer master data
        alert_days: Days before expiration to alert (default from config)

    Returns:
        DataFrame with customers to contact for renewal

    Example:
        >>> renewals = generate_renewals_list(anagrafica_df, alert_days=90)
    """
    if alert_days is None:
        alert_days = WORK_PARAMS["renewal_alert_days"]

    # Get today's date
    today = datetime.now()
    alert_date = today + timedelta(days=alert_days)

    # Convert data riferimento to datetime
    anagrafica_df["Data_Riferimento_DT"] = pd.to_datetime(
        anagrafica_df["Data visita di riferimento 2026"], errors="coerce"
    )

    # Filter contracts expiring within alert_days
    renewals = anagrafica_df[
        (anagrafica_df["Data_Riferimento_DT"] <= alert_date)
        & (anagrafica_df["Data_Riferimento_DT"] >= today)
    ].copy()

    # Calculate days to expiration
    renewals["Giorni_a_Scadenza"] = (
        renewals["Data_Riferimento_DT"] - today
    ).dt.days

    # Prepare output columns
    renewals_output = pd.DataFrame(
        {
            "ID_Cliente": renewals["ID Cliente"],
            "Cliente": renewals["Nome del Cliente"],
            "Indirizzo": renewals["Indirizzo completo"],
            "Città": renewals["Città"],
            "Regione": renewals["Regione"],
            "Data_Scadenza_2026": renewals["Data visita di riferimento 2026"],
            "Giorni_a_Scadenza": renewals["Giorni_a_Scadenza"],
            "Stato_Contatto": "",
            "Data_Contatto": "",
            "Ordine_Ricevuto": "",
            "Note": "",
        }
    )

    # Sort by days to expiration
    renewals_output = renewals_output.sort_values("Giorni_a_Scadenza")

    return renewals_output


# ============================================================================
# MAIN PLANNING ORCHESTRATION
# ============================================================================


def generate_planning(
    anagrafica_df: pd.DataFrame,
    ordini_df: pd.DataFrame,
    n_clusters: int = None,
    progress_callback=None,
) -> Dict[str, any]:
    """
    Generate complete inspection planning.

    Orchestrates all steps:
    1. Match orders with customer data
    2. Geocode addresses
    3. Cluster geographically
    4. Assign inspectors
    5. Generate optimized tours
    6. Create renewals list

    Args:
        anagrafica_df: Customer master data
        ordini_df: Confirmed orders
        n_clusters: Number of geographic clusters
        progress_callback: Progress callback function(step, message)

    Returns:
        Dictionary with:
        - planning: Complete planning DataFrame
        - renewals: Renewals list DataFrame
        - unmatched_orders: Unmatched orders DataFrame
        - stats: Statistics dictionary

    Example:
        >>> result = generate_planning(
        ...     anagrafica_df,
        ...     ordini_df,
        ...     progress_callback=lambda s, m: print(f"{s}: {m}")
        ... )
        >>> planning_df = result["planning"]
    """
    results = {}

    # Step 1: Match orders
    if progress_callback:
        progress_callback(1, "Matching ordini con anagrafica...")

    matched, unmatched = match_orders(anagrafica_df, ordini_df)
    results["unmatched_orders"] = unmatched

    if len(matched) == 0:
        raise ValueError(
            "Nessun ordine matchato! Verificare che Cliente e Indirizzo "
            "corrispondano esattamente tra anagrafica e ordini."
        )

    # Step 2: Geocode addresses
    if progress_callback:
        progress_callback(2, "Geocodifica indirizzi...")

    matched = geocode_addresses(matched, progress_callback)

    # Step 3: Geographic clustering
    if progress_callback:
        progress_callback(3, "Clustering geografico...")

    matched = cluster_geographic(matched, n_clusters)

    # Step 4: Assign inspectors
    if progress_callback:
        progress_callback(4, "Assegnazione ispettori...")

    matched = assign_inspectors(matched)

    # Step 5: Generate tours
    if progress_callback:
        progress_callback(5, "Generazione tour ottimizzati...")

    planning = generate_tours(matched)
    results["planning"] = planning

    # Step 6: Generate renewals list
    if progress_callback:
        progress_callback(6, "Generazione lista rinnovi...")

    renewals = generate_renewals_list(anagrafica_df)
    results["renewals"] = renewals

    # Calculate statistics
    results["stats"] = {
        "ordini_totali": len(ordini_df),
        "ordini_matchati": len(matched),
        "ordini_non_matchati": len(unmatched),
        "visite_pianificate": len(planning),
        "ispettori_attivi": planning["Ispettore"].nunique() if len(planning) > 0 else 0,
        "settimane_necessarie": (
            planning["Settimana"].nunique() if len(planning) > 0 else 0
        ),
        "km_totali": planning["km_from_previous"].sum() if len(planning) > 0 else 0,
        "rinnovi_da_contattare": len(renewals),
    }

    return results


# ============================================================================
# PLANNING MODIFICATIONS
# ============================================================================


def update_inspector_assignment(
    planning_df: pd.DataFrame,
    visit_index: int,
    new_inspector: str,
    region: str,
) -> Tuple[bool, str, pd.DataFrame]:
    """
    Update inspector assignment for a specific visit.

    Validates Paolo constraint before updating.

    Args:
        planning_df: Planning DataFrame
        visit_index: Index of visit to update
        new_inspector: New inspector name
        region: Region of the visit

    Returns:
        Tuple of (success, message, updated_df)

    Example:
        >>> success, msg, updated = update_inspector_assignment(
        ...     planning_df, 5, "Paolo", "Lombardia"
        ... )
    """
    # Validate assignment
    is_valid, message = validate_inspector_assignment(new_inspector, region)

    if not is_valid:
        return False, message, planning_df

    # Update assignment
    updated_df = planning_df.copy()
    updated_df.at[visit_index, "Ispettore"] = new_inspector

    return True, message if message else "Assegnazione aggiornata", updated_df
