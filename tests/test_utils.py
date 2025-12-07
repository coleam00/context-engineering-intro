"""
Unit tests for utils.py functions.

Tests string normalization, distance calculations, date utilities, and validation.
"""

import pytest
from datetime import datetime, timedelta
import pandas as pd

from utils import (
    normalize_string,
    match_strings_fuzzy,
    calculate_distance,
    calculate_travel_time,
    is_weekend,
    is_holiday,
    is_available,
    next_available_date,
    get_week_number,
    get_day_name_italian,
    validate_anagrafica_columns,
    validate_ordini_columns,
    format_duration,
    format_distance,
)


# ============================================================================
# STRING NORMALIZATION TESTS
# ============================================================================


def test_normalize_string_basic():
    """Test basic string normalization."""
    assert normalize_string("  hello  world  ") == "HELLO WORLD"


def test_normalize_string_uppercase():
    """Test uppercase conversion."""
    assert normalize_string("via roma") == "VIA ROMA"


def test_normalize_string_whitespace():
    """Test whitespace collapsing."""
    assert normalize_string("via   roma   1") == "VIA ROMA 1"


def test_normalize_string_empty():
    """Test empty string handling."""
    assert normalize_string("") == ""


def test_normalize_string_none():
    """Test None handling."""
    assert normalize_string(None) == ""


def test_match_strings_fuzzy_exact():
    """Test exact match after normalization."""
    assert match_strings_fuzzy("  Via Roma  ", "via roma") is True


def test_match_strings_fuzzy_different():
    """Test different strings."""
    assert match_strings_fuzzy("Via Roma", "Via Milano") is False


# ============================================================================
# DISTANCE CALCULATION TESTS
# ============================================================================


def test_calculate_distance_same_point():
    """Test distance between same point."""
    coord = (46.08, 13.18)
    assert calculate_distance(coord, coord) == pytest.approx(0.0, abs=0.1)


def test_calculate_distance_known():
    """Test known distance (Udine to Milano approx 318km)."""
    udine = (46.08, 13.18)
    milano = (45.46, 9.19)
    distance = calculate_distance(udine, milano)
    assert 310 < distance < 325  # Approximate range


def test_calculate_travel_time():
    """Test travel time calculation."""
    # 140 km at 70 km/h = 2 hours
    time_hours = calculate_travel_time(140, 70)
    assert time_hours == pytest.approx(2.0, abs=0.01)


def test_calculate_travel_time_default_speed():
    """Test travel time with default speed."""
    # Should use speed from config (70 km/h)
    time_hours = calculate_travel_time(140)
    assert time_hours == pytest.approx(2.0, abs=0.01)


# ============================================================================
# DATE & TIME TESTS
# ============================================================================


def test_is_weekend_saturday():
    """Test Saturday detection."""
    saturday = datetime(2025, 12, 13)  # Saturday
    assert is_weekend(saturday) is True


def test_is_weekend_sunday():
    """Test Sunday detection."""
    sunday = datetime(2025, 12, 14)  # Sunday
    assert is_weekend(sunday) is True


def test_is_weekend_monday():
    """Test Monday is not weekend."""
    monday = datetime(2025, 12, 15)  # Monday
    assert is_weekend(monday) is False


def test_is_holiday_christmas():
    """Test Christmas holiday detection."""
    christmas = datetime(2025, 12, 25)
    assert is_holiday(christmas) is True


def test_is_holiday_new_year():
    """Test New Year holiday detection."""
    new_year = datetime(2026, 1, 1)
    assert is_holiday(new_year) is True


def test_is_holiday_normal_day():
    """Test normal working day."""
    normal_day = datetime(2025, 12, 10)
    assert is_holiday(normal_day) is False


def test_is_available_weekend():
    """Test weekend is not available."""
    saturday = datetime(2025, 12, 13)
    available, reason = is_available(saturday)
    assert available is False
    assert reason == "Weekend"


def test_is_available_holiday():
    """Test holiday is not available."""
    christmas = datetime(2025, 12, 25)
    available, reason = is_available(christmas)
    assert available is False
    assert reason == "Festività"


def test_is_available_working_day():
    """Test normal working day is available."""
    working_day = datetime(2025, 12, 10)  # Wednesday
    available, reason = is_available(working_day)
    assert available is True
    assert reason is None


def test_next_available_date_from_saturday():
    """Test finding next available date from Saturday."""
    saturday = datetime(2025, 12, 13)
    next_date = next_available_date(saturday)
    # Should skip to Monday
    assert next_date.weekday() == 0  # Monday
    assert next_date.day == 15


def test_get_week_number():
    """Test ISO week number calculation."""
    date = datetime(2025, 12, 10)
    week = get_week_number(date)
    assert isinstance(week, int)
    assert 1 <= week <= 53


def test_get_day_name_italian_monday():
    """Test Italian day name for Monday."""
    monday = datetime(2025, 12, 15)
    assert get_day_name_italian(monday) == "Lunedì"


def test_get_day_name_italian_friday():
    """Test Italian day name for Friday."""
    friday = datetime(2025, 12, 19)
    assert get_day_name_italian(friday) == "Venerdì"


# ============================================================================
# VALIDATION TESTS
# ============================================================================


def test_validate_anagrafica_columns_valid():
    """Test validation with all required columns."""
    df = pd.DataFrame(
        {
            "ID Cliente": [1],
            "Nome del Cliente": ["Test"],
            "Indirizzo completo": ["Via Roma 1"],
            "CAP": ["33100"],
            "Città": ["Udine"],
            "Regione": ["Friuli-Venezia Giulia"],
            "Ore lavoro": [2.5],
            "Data visita di riferimento 2026": ["2026-03-15"],
        }
    )
    is_valid, missing = validate_anagrafica_columns(df)
    assert is_valid is True
    assert len(missing) == 0


def test_validate_anagrafica_columns_missing():
    """Test validation with missing columns."""
    df = pd.DataFrame({"ID Cliente": [1], "Nome del Cliente": ["Test"]})
    is_valid, missing = validate_anagrafica_columns(df)
    assert is_valid is False
    assert len(missing) > 0


def test_validate_ordini_columns_valid():
    """Test validation with all required ordini columns."""
    df = pd.DataFrame(
        {
            "ID_Ordine": ["ORD001"],
            "Cliente": ["Test"],
            "Indirizzo_Sede": ["Via Roma 1"],
        }
    )
    is_valid, missing = validate_ordini_columns(df)
    assert is_valid is True
    assert len(missing) == 0


def test_validate_ordini_columns_missing():
    """Test validation with missing ordini columns."""
    df = pd.DataFrame({"ID_Ordine": ["ORD001"]})
    is_valid, missing = validate_ordini_columns(df)
    assert is_valid is False
    assert len(missing) > 0


# ============================================================================
# FORMATTING TESTS
# ============================================================================


def test_format_duration_whole_hours():
    """Test formatting whole hours."""
    assert format_duration(3.0) == "3h 00min"


def test_format_duration_with_minutes():
    """Test formatting hours and minutes."""
    assert format_duration(2.5) == "2h 30min"


def test_format_distance():
    """Test distance formatting."""
    assert format_distance(145.7) == "145.7 km"


def test_format_distance_round():
    """Test distance formatting with rounding."""
    formatted = format_distance(145.678)
    assert "145.7" in formatted
    assert "km" in formatted
