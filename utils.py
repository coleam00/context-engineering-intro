"""
Utility functions for Modulblok Inspection Planning System.

Provides helper functions for data processing, calculations, and formatting.
"""

import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

import pandas as pd
from geopy.distance import geodesic

from config import (
    COLORS,
    EMAIL_TEMPLATE,
    ITALIAN_HOLIDAYS,
    PLANNING_COLUMNS,
    RENEWALS_COLUMNS,
    WORK_PARAMS,
)


# ============================================================================
# STRING NORMALIZATION
# ============================================================================


def normalize_string(text: str) -> str:
    """
    Normalize string for robust matching.

    Performs:
    - Convert to uppercase
    - Strip leading/trailing whitespace
    - Collapse multiple spaces to single space
    - Remove special characters

    Args:
        text: Input string

    Returns:
        Normalized string

    Example:
        >>> normalize_string("  Via  Roma,  1  ")
        "VIA ROMA, 1"
    """
    if not isinstance(text, str):
        return ""

    # Convert to uppercase
    text = text.upper()

    # Strip whitespace
    text = text.strip()

    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text


def match_strings_fuzzy(str1: str, str2: str, threshold: float = 0.9) -> bool:
    """
    Check if two strings match with fuzzy logic.

    Args:
        str1: First string
        str2: Second string
        threshold: Similarity threshold (0-1)

    Returns:
        True if strings match above threshold
    """
    # Normalize both strings
    norm1 = normalize_string(str1)
    norm2 = normalize_string(str2)

    # Exact match after normalization
    if norm1 == norm2:
        return True

    # Simple similarity: length ratio
    if len(norm1) == 0 or len(norm2) == 0:
        return False

    # Count matching characters
    matches = sum(1 for a, b in zip(norm1, norm2) if a == b)
    max_len = max(len(norm1), len(norm2))
    similarity = matches / max_len

    return similarity >= threshold


# ============================================================================
# DISTANCE CALCULATIONS
# ============================================================================


def calculate_distance(
    coord1: Tuple[float, float], coord2: Tuple[float, float]
) -> float:
    """
    Calculate geodesic distance between two coordinates.

    Args:
        coord1: (latitude, longitude) tuple
        coord2: (latitude, longitude) tuple

    Returns:
        Distance in kilometers

    Example:
        >>> calculate_distance((46.08, 13.18), (45.46, 9.19))
        280.5
    """
    try:
        return geodesic(coord1, coord2).kilometers
    except Exception as e:
        print(f"Error calculating distance: {e}")
        return 0.0


def calculate_travel_time(distance_km: float, speed_kmh: float = None) -> float:
    """
    Calculate travel time based on distance.

    Args:
        distance_km: Distance in kilometers
        speed_kmh: Average speed (default from config)

    Returns:
        Travel time in hours

    Example:
        >>> calculate_travel_time(140, 70)
        2.0
    """
    if speed_kmh is None:
        speed_kmh = WORK_PARAMS["average_speed_kmh"]

    if speed_kmh <= 0:
        return 0.0

    return distance_km / speed_kmh


# ============================================================================
# DATE & TIME UTILITIES
# ============================================================================


def is_weekend(date: datetime) -> bool:
    """
    Check if a date falls on weekend.

    Args:
        date: Date to check

    Returns:
        True if Saturday or Sunday

    Example:
        >>> is_weekend(datetime(2025, 12, 13))  # Saturday
        True
    """
    return date.weekday() >= 5  # Saturday=5, Sunday=6


def is_holiday(date: datetime, custom_holidays: List[datetime] = None) -> bool:
    """
    Check if a date is a holiday.

    Args:
        date: Date to check
        custom_holidays: Additional custom holiday dates

    Returns:
        True if date is a holiday

    Example:
        >>> is_holiday(datetime(2025, 12, 25))  # Christmas
        True
    """
    date_str = date.strftime("%Y-%m-%d")

    # Check Italian national holidays
    for holiday_date, _ in ITALIAN_HOLIDAYS:
        if holiday_date == date_str:
            return True

    # Check custom holidays
    if custom_holidays:
        for custom_date in custom_holidays:
            if custom_date.strftime("%Y-%m-%d") == date_str:
                return True

    return False


def is_available(
    date: datetime,
    inspector: str = None,
    vacations_df: pd.DataFrame = None,
    custom_holidays: List[datetime] = None,
) -> Tuple[bool, Optional[str]]:
    """
    Check if a date is available for work.

    Checks:
    - Not a weekend
    - Not a holiday
    - Inspector not on vacation (if specified)

    Args:
        date: Date to check
        inspector: Inspector name (optional)
        vacations_df: DataFrame with vacation data
        custom_holidays: Additional holiday dates

    Returns:
        Tuple of (is_available, reason if not available)

    Example:
        >>> is_available(datetime(2025, 12, 13))
        (False, "Weekend")
    """
    # Check weekend
    if is_weekend(date):
        return False, "Weekend"

    # Check holidays
    if is_holiday(date, custom_holidays):
        return False, "Festività"

    # Check inspector vacations
    if inspector and vacations_df is not None:
        inspector_vacations = vacations_df[vacations_df["Ispettore"] == inspector]

        for _, vacation in inspector_vacations.iterrows():
            start_date = pd.to_datetime(vacation["Data_Inizio"])
            end_date = pd.to_datetime(vacation["Data_Fine"])

            if start_date <= date <= end_date:
                vacation_type = vacation.get("Tipo", "Ferie")
                return False, vacation_type

    return True, None


def next_available_date(
    start_date: datetime,
    inspector: str = None,
    vacations_df: pd.DataFrame = None,
    custom_holidays: List[datetime] = None,
    max_days: int = 365,
) -> datetime:
    """
    Find the next available working date.

    Args:
        start_date: Starting date
        inspector: Inspector name (optional)
        vacations_df: Vacation data
        custom_holidays: Custom holidays
        max_days: Maximum days to search ahead

    Returns:
        Next available date

    Example:
        >>> next_available_date(datetime(2025, 12, 13))  # Saturday
        datetime(2025, 12, 15)  # Monday
    """
    current_date = start_date

    for _ in range(max_days):
        available, _ = is_available(
            current_date, inspector, vacations_df, custom_holidays
        )

        if available:
            return current_date

        current_date += timedelta(days=1)

    # Fallback: return start date if no available date found
    return start_date


def get_week_number(date: datetime) -> int:
    """
    Get ISO week number for a date.

    Args:
        date: Date

    Returns:
        Week number (1-53)
    """
    return date.isocalendar()[1]


def get_day_name_italian(date: datetime) -> str:
    """
    Get Italian day name for a date.

    Args:
        date: Date

    Returns:
        Italian day name
    """
    days = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
    return days[date.weekday()]


# ============================================================================
# EMAIL GENERATION
# ============================================================================


def generate_email(visit_data: Dict[str, any]) -> str:
    """
    Generate email text for a visit confirmation.

    Args:
        visit_data: Dictionary with visit information

    Returns:
        Formatted email text

    Example:
        >>> data = {
        ...     "cliente": "FORMA CUCINE SPA",
        ...     "data": "2025-12-15",
        ...     "indirizzo": "Via Roma 1",
        ...     "citta": "Venezia",
        ...     "ore": 3.5,
        ...     "ispettore": "Adrian"
        ... }
        >>> email = generate_email(data)
    """
    # Format date
    if isinstance(visit_data.get("data"), str):
        date_obj = pd.to_datetime(visit_data["data"])
    else:
        date_obj = visit_data.get("data")

    date_formatted = date_obj.strftime("%d/%m/%Y")

    # Format email
    email_text = EMAIL_TEMPLATE.format(
        cliente=visit_data.get("cliente", ""),
        data=date_formatted,
        indirizzo=visit_data.get("indirizzo", ""),
        citta=visit_data.get("citta", ""),
        ore=visit_data.get("ore", 0),
        ispettore=visit_data.get("ispettore", ""),
    )

    return email_text


def generate_bulk_emails(visits_df: pd.DataFrame) -> List[Dict[str, str]]:
    """
    Generate emails for multiple visits.

    Args:
        visits_df: DataFrame with visit data

    Returns:
        List of dictionaries with {cliente, email_text}
    """
    emails = []

    for _, visit in visits_df.iterrows():
        visit_dict = visit.to_dict()
        email_text = generate_email(visit_dict)

        emails.append({"cliente": visit.get("Cliente", ""), "email": email_text})

    return emails


# ============================================================================
# EXCEL EXPORT
# ============================================================================


def format_planning_excel(
    planning_df: pd.DataFrame, output_path: str, inspectors: List[str]
) -> None:
    """
    Export planning to Excel with multiple sheets.

    Creates:
    - Sheet 1: Complete planning
    - Sheets 2-5: Individual inspector views
    - Sheet 6: KPIs

    Args:
        planning_df: Planning DataFrame
        output_path: Output file path
        inspectors: List of inspector names

    Returns:
        None (writes file)
    """
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        # Sheet 1: Complete planning
        planning_df.to_excel(writer, sheet_name="Planning_Tour", index=False)

        # Sheets 2-5: Individual inspectors
        for inspector in inspectors:
            inspector_df = planning_df[planning_df["Ispettore"] == inspector]
            sheet_name = f"Planning_{inspector}"
            inspector_df.to_excel(writer, sheet_name=sheet_name, index=False)

        # Sheet 6: KPIs
        kpis = calculate_kpis(planning_df)
        kpis_df = pd.DataFrame([kpis])
        kpis_df.to_excel(writer, sheet_name="KPI", index=False)


def format_renewals_excel(renewals_df: pd.DataFrame, output_path: str) -> None:
    """
    Export renewals list to Excel.

    Args:
        renewals_df: Renewals DataFrame
        output_path: Output file path

    Returns:
        None (writes file)
    """
    # Ensure correct columns
    for col in RENEWALS_COLUMNS:
        if col not in renewals_df.columns:
            renewals_df[col] = ""

    # Select and order columns
    renewals_df = renewals_df[RENEWALS_COLUMNS]

    # Export
    renewals_df.to_excel(output_path, index=False, engine="openpyxl")


# ============================================================================
# STATISTICS & KPIs
# ============================================================================


def calculate_kpis(planning_df: pd.DataFrame) -> Dict[str, any]:
    """
    Calculate KPIs from planning data.

    Args:
        planning_df: Planning DataFrame

    Returns:
        Dictionary with KPI values

    Example:
        >>> kpis = calculate_kpis(planning_df)
        >>> print(kpis["visite_totali"])
        49
    """
    kpis = {
        "visite_totali": len(planning_df),
        "ispettori_attivi": planning_df["Ispettore"].nunique(),
        "km_totali": planning_df["Km_da_Precedente"].sum(),
        "ore_totali": planning_df["Ore_Stimate"].sum(),
        "settimane_necessarie": planning_df["Settimana"].nunique(),
        "media_km_per_visita": (
            planning_df["Km_da_Precedente"].mean() if len(planning_df) > 0 else 0
        ),
        "media_ore_per_visita": (
            planning_df["Ore_Stimate"].mean() if len(planning_df) > 0 else 0
        ),
    }

    # Per-inspector stats
    for inspector in planning_df["Ispettore"].unique():
        inspector_df = planning_df[planning_df["Ispettore"] == inspector]
        kpis[f"{inspector}_visite"] = len(inspector_df)
        kpis[f"{inspector}_km"] = inspector_df["Km_da_Precedente"].sum()
        kpis[f"{inspector}_ore"] = inspector_df["Ore_Stimate"].sum()

    return kpis


def get_visits_by_inspector(planning_df: pd.DataFrame) -> pd.DataFrame:
    """
    Get visit count by inspector.

    Args:
        planning_df: Planning DataFrame

    Returns:
        DataFrame with inspector statistics
    """
    stats = (
        planning_df.groupby("Ispettore")
        .agg(
            {
                "Cliente": "count",
                "Km_da_Precedente": "sum",
                "Ore_Stimate": "sum",
                "Data": lambda x: x.nunique(),
            }
        )
        .rename(
            columns={
                "Cliente": "Visite",
                "Km_da_Precedente": "Km Totali",
                "Ore_Stimate": "Ore Totali",
                "Data": "Giorni",
            }
        )
    )

    return stats.reset_index()


def get_visits_by_region(planning_df: pd.DataFrame) -> pd.DataFrame:
    """
    Get visit count by region.

    Args:
        planning_df: Planning DataFrame

    Returns:
        DataFrame with regional statistics
    """
    stats = (
        planning_df.groupby("Regione")
        .agg({"Cliente": "count", "Km_da_Precedente": "sum"})
        .rename(columns={"Cliente": "Visite", "Km_da_Precedente": "Km Totali"})
        .sort_values("Visite", ascending=False)
    )

    return stats.reset_index()


# ============================================================================
# DATA VALIDATION
# ============================================================================


def validate_anagrafica_columns(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Validate that DataFrame has required anagrafica columns.

    Args:
        df: Input DataFrame

    Returns:
        Tuple of (is_valid, list of missing columns)
    """
    required_columns = [
        "ID Cliente",
        "Nome del Cliente",
        "Indirizzo completo",
        "CAP",
        "Città",
        "Regione",
        "Ore lavoro",
        "Data visita di riferimento 2026",
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]

    return len(missing_columns) == 0, missing_columns


def validate_ordini_columns(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Validate that DataFrame has required ordini columns.

    Args:
        df: Input DataFrame

    Returns:
        Tuple of (is_valid, list of missing columns)
    """
    required_columns = ["ID_Ordine", "Cliente", "Indirizzo_Sede"]

    missing_columns = [col for col in required_columns if col not in df.columns]

    return len(missing_columns) == 0, missing_columns


# ============================================================================
# FORMATTING UTILITIES
# ============================================================================


def format_duration(hours: float) -> str:
    """
    Format duration in hours to human-readable string.

    Args:
        hours: Duration in hours

    Returns:
        Formatted string

    Example:
        >>> format_duration(2.5)
        "2h 30min"
    """
    h = int(hours)
    m = int((hours - h) * 60)
    return f"{h}h {m:02d}min"


def format_distance(km: float) -> str:
    """
    Format distance in km to human-readable string.

    Args:
        km: Distance in kilometers

    Returns:
        Formatted string

    Example:
        >>> format_distance(145.7)
        "145.7 km"
    """
    return f"{km:.1f} km"


def truncate_text(text: str, max_length: int = 50) -> str:
    """
    Truncate text to maximum length.

    Args:
        text: Input text
        max_length: Maximum length

    Returns:
        Truncated text with ellipsis if needed

    Example:
        >>> truncate_text("Very long customer name here", 20)
        "Very long customer..."
    """
    if len(text) <= max_length:
        return text

    return text[: max_length - 3] + "..."
