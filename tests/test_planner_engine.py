"""
Unit tests for planner_engine.py functions.

Tests order matching, inspector assignment, TSP optimization, and scheduling.
"""

import pytest
from datetime import datetime
import pandas as pd

from planner_engine import (
    match_orders,
    cluster_geographic,
    tsp_nearest_neighbor,
    assign_inspectors,
    schedule_daily,
    generate_renewals_list,
    update_inspector_assignment,
)
from config import PAOLO_REGIONS


# ============================================================================
# ORDER MATCHING TESTS
# ============================================================================


def test_match_orders_exact():
    """Test exact order matching."""
    anagrafica = pd.DataFrame(
        {
            "ID Cliente": [1],
            "Nome del Cliente": ["CLIENTE TEST"],
            "Indirizzo completo": ["VIA ROMA 1"],
            "Città": ["Udine"],
            "Regione": ["Friuli-Venezia Giulia"],
            "Ore lavoro": [2.5],
            "Data visita di riferimento 2026": ["2026-03-15"],
            "CAP": ["33100"],
        }
    )

    ordini = pd.DataFrame(
        {
            "ID_Ordine": ["ORD001"],
            "Cliente": ["CLIENTE TEST"],
            "Indirizzo_Sede": ["VIA ROMA 1"],
        }
    )

    matched, unmatched = match_orders(anagrafica, ordini)

    assert len(matched) == 1
    assert len(unmatched) == 0


def test_match_orders_case_insensitive():
    """Test case-insensitive matching."""
    anagrafica = pd.DataFrame(
        {
            "ID Cliente": [1],
            "Nome del Cliente": ["Cliente Test"],
            "Indirizzo completo": ["via roma 1"],
            "Città": ["Udine"],
            "Regione": ["Friuli-Venezia Giulia"],
            "Ore lavoro": [2.5],
            "Data visita di riferimento 2026": ["2026-03-15"],
            "CAP": ["33100"],
        }
    )

    ordini = pd.DataFrame(
        {
            "ID_Ordine": ["ORD001"],
            "Cliente": ["CLIENTE TEST"],
            "Indirizzo_Sede": ["VIA ROMA 1"],
        }
    )

    matched, unmatched = match_orders(anagrafica, ordini)

    assert len(matched) == 1
    assert len(unmatched) == 0


def test_match_orders_whitespace():
    """Test matching with extra whitespace."""
    anagrafica = pd.DataFrame(
        {
            "ID Cliente": [1],
            "Nome del Cliente": ["  Cliente  Test  "],
            "Indirizzo completo": ["  Via  Roma  1  "],
            "Città": ["Udine"],
            "Regione": ["Friuli-Venezia Giulia"],
            "Ore lavoro": [2.5],
            "Data visita di riferimento 2026": ["2026-03-15"],
            "CAP": ["33100"],
        }
    )

    ordini = pd.DataFrame(
        {
            "ID_Ordine": ["ORD001"],
            "Cliente": ["Cliente Test"],
            "Indirizzo_Sede": ["Via Roma 1"],
        }
    )

    matched, unmatched = match_orders(anagrafica, ordini)

    assert len(matched) == 1
    assert len(unmatched) == 0


def test_match_orders_no_match():
    """Test when no orders match."""
    anagrafica = pd.DataFrame(
        {
            "ID Cliente": [1],
            "Nome del Cliente": ["CLIENTE A"],
            "Indirizzo completo": ["VIA ROMA 1"],
            "Città": ["Udine"],
            "Regione": ["Friuli-Venezia Giulia"],
            "Ore lavoro": [2.5],
            "Data visita di riferimento 2026": ["2026-03-15"],
            "CAP": ["33100"],
        }
    )

    ordini = pd.DataFrame(
        {
            "ID_Ordine": ["ORD001"],
            "Cliente": ["CLIENTE B"],
            "Indirizzo_Sede": ["VIA MILANO 1"],
        }
    )

    matched, unmatched = match_orders(anagrafica, ordini)

    assert len(matched) == 0
    assert len(unmatched) == 1


# ============================================================================
# CLUSTERING TESTS
# ============================================================================


def test_cluster_geographic_basic():
    """Test basic geographic clustering."""
    df = pd.DataFrame(
        {
            "lat": [46.08, 46.06, 45.46, 45.44],
            "lon": [13.18, 13.24, 9.19, 9.25],
        }
    )

    clustered = cluster_geographic(df, n_clusters=2)

    assert "cluster_id" in clustered.columns
    assert clustered["cluster_id"].nunique() == 2


def test_cluster_geographic_single_cluster():
    """Test clustering with only one client."""
    df = pd.DataFrame({"lat": [46.08], "lon": [13.18]})

    clustered = cluster_geographic(df, n_clusters=8)

    assert "cluster_id" in clustered.columns
    assert clustered["cluster_id"].iloc[0] == 0


# ============================================================================
# TSP OPTIMIZATION TESTS
# ============================================================================


def test_tsp_nearest_neighbor_basic():
    """Test TSP optimization with basic data."""
    clients = pd.DataFrame(
        {
            "lat": [46.08, 46.06, 45.46],
            "lon": [13.18, 13.24, 9.19],
            "Nome del Cliente": ["Cliente A", "Cliente B", "Cliente C"],
        }
    )

    base_coords = (46.08, 13.18)
    optimized = tsp_nearest_neighbor(clients, base_coords)

    assert len(optimized) == 3
    assert "km_from_previous" in optimized.columns
    # First client should be closest to base (Cliente A at base coords)
    assert optimized.iloc[0]["km_from_previous"] < 10  # Very close


def test_tsp_nearest_neighbor_empty():
    """Test TSP with empty DataFrame."""
    clients = pd.DataFrame()
    base_coords = (46.08, 13.18)

    optimized = tsp_nearest_neighbor(clients, base_coords)

    assert len(optimized) == 0


# ============================================================================
# INSPECTOR ASSIGNMENT TESTS
# ============================================================================


def test_assign_inspectors_paolo_region():
    """Test Paolo is assigned to his regions."""
    df = pd.DataFrame({"Regione": ["Lombardia", "Piemonte", "Liguria"]})

    assigned = assign_inspectors(df)

    assert "Ispettore" in assigned.columns
    # All should be assigned to Paolo
    assert all(assigned["Ispettore"] == "Paolo")


def test_assign_inspectors_national_region():
    """Test national regions get other inspectors."""
    df = pd.DataFrame({"Regione": ["Toscana", "Veneto", "Lazio"]})

    assigned = assign_inspectors(df)

    assert "Ispettore" in assigned.columns
    # None should be Paolo
    assert all(assigned["Ispettore"] != "Paolo")
    # Should be one of the national inspectors
    assert all(assigned["Ispettore"].isin(["Adrian", "Salvatore", "Mattia"]))


def test_assign_inspectors_mixed_regions():
    """Test mixed regions."""
    df = pd.DataFrame({"Regione": ["Lombardia", "Toscana", "Piemonte", "Veneto"]})

    assigned = assign_inspectors(df)

    # Paolo regions should have Paolo
    paolo_rows = assigned[assigned["Regione"].isin(PAOLO_REGIONS)]
    assert all(paolo_rows["Ispettore"] == "Paolo")

    # Non-Paolo regions should NOT have Paolo
    non_paolo_rows = assigned[~assigned["Regione"].isin(PAOLO_REGIONS)]
    assert all(non_paolo_rows["Ispettore"] != "Paolo")


# ============================================================================
# SCHEDULING TESTS
# ============================================================================


def test_schedule_daily_basic():
    """Test basic daily scheduling."""
    clients = pd.DataFrame(
        {
            "Nome del Cliente": ["Cliente A", "Cliente B"],
            "Ore lavoro": [3.0, 4.0],
            "km_from_previous": [50, 30],
            "lat": [46.08, 46.06],
            "lon": [13.18, 13.24],
        }
    )

    start_date = datetime(2025, 12, 9)  # Monday
    scheduled = schedule_daily(clients, "Adrian", start_date)

    assert "Data" in scheduled.columns
    assert "Settimana" in scheduled.columns
    assert "Giorno" in scheduled.columns
    assert len(scheduled) == 2


def test_schedule_daily_weekend_skip():
    """Test that weekends are skipped."""
    clients = pd.DataFrame(
        {
            "Nome del Cliente": ["Cliente A"],
            "Ore lavoro": [3.0],
            "km_from_previous": [50],
            "lat": [46.08],
            "lon": [13.18],
        }
    )

    start_date = datetime(2025, 12, 13)  # Saturday
    scheduled = schedule_daily(clients, "Adrian", start_date)

    # Should be scheduled on Monday
    scheduled_date = scheduled.iloc[0]["Data"]
    assert scheduled_date.weekday() == 0  # Monday


def test_schedule_daily_8h_limit():
    """Test that 8-hour daily limit is respected."""
    # Create visits that would exceed 8 hours in one day
    clients = pd.DataFrame(
        {
            "Nome del Cliente": ["Cliente A", "Cliente B"],
            "Ore lavoro": [5.0, 5.0],  # 10 hours total (+ buffer)
            "km_from_previous": [10, 10],
            "lat": [46.08, 46.06],
            "lon": [13.18, 13.24],
        }
    )

    start_date = datetime(2025, 12, 9)  # Monday
    scheduled = schedule_daily(clients, "Adrian", start_date)

    # Should be scheduled on different days
    dates = scheduled["Data"].unique()
    assert len(dates) >= 2


# ============================================================================
# RENEWALS LIST TESTS
# ============================================================================


def test_generate_renewals_list_within_90_days():
    """Test renewals list generation for contracts expiring within 90 days."""
    # Create test data with various expiration dates
    today = datetime.now()
    future_60_days = (today + pd.Timedelta(days=60)).strftime("%Y-%m-%d")
    future_120_days = (today + pd.Timedelta(days=120)).strftime("%Y-%m-%d")

    anagrafica = pd.DataFrame(
        {
            "ID Cliente": [1, 2],
            "Nome del Cliente": ["Cliente A", "Cliente B"],
            "Indirizzo completo": ["Via Roma 1", "Via Milano 2"],
            "Città": ["Udine", "Milano"],
            "Regione": ["Friuli-Venezia Giulia", "Lombardia"],
            "Data visita di riferimento 2026": [future_60_days, future_120_days],
            "CAP": ["33100", "20100"],
            "Ore lavoro": [2.5, 3.0],
        }
    )

    renewals = generate_renewals_list(anagrafica, alert_days=90)

    # Only Cliente A should be in renewals (within 90 days)
    assert len(renewals) == 1
    assert renewals.iloc[0]["Cliente"] == "Cliente A"


# ============================================================================
# INSPECTOR ASSIGNMENT UPDATE TESTS
# ============================================================================


def test_update_inspector_assignment_valid():
    """Test valid inspector assignment update."""
    planning = pd.DataFrame(
        {
            "Ispettore": ["Adrian"],
            "Regione": ["Toscana"],
            "Nome del Cliente": ["Cliente A"],
        }
    )

    success, message, updated = update_inspector_assignment(
        planning, 0, "Salvatore", "Toscana"
    )

    assert success is True
    assert updated.iloc[0]["Ispettore"] == "Salvatore"


def test_update_inspector_assignment_paolo_wrong_region():
    """Test Paolo cannot be assigned to wrong region."""
    planning = pd.DataFrame(
        {
            "Ispettore": ["Adrian"],
            "Regione": ["Toscana"],
            "Nome del Cliente": ["Cliente A"],
        }
    )

    success, message, updated = update_inspector_assignment(
        planning, 0, "Paolo", "Toscana"
    )

    assert success is False
    assert "Paolo" in message


def test_update_inspector_assignment_paolo_correct_region():
    """Test Paolo can be assigned to his regions."""
    planning = pd.DataFrame(
        {
            "Ispettore": ["Adrian"],
            "Regione": ["Lombardia"],
            "Nome del Cliente": ["Cliente A"],
        }
    )

    success, message, updated = update_inspector_assignment(
        planning, 0, "Paolo", "Lombardia"
    )

    assert success is True
    assert updated.iloc[0]["Ispettore"] == "Paolo"
