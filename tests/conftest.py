"""
Pytest configuration and fixtures for testing.

Provides common test data and fixtures used across test modules.
"""

import pytest
import pandas as pd
from datetime import datetime


@pytest.fixture
def sample_anagrafica():
    """Sample customer master data for testing."""
    return pd.DataFrame(
        {
            "ID Cliente": [1, 2, 3, 4, 5],
            "Nome del Cliente": [
                "CLIENTE A",
                "CLIENTE B",
                "CLIENTE C",
                "CLIENTE D",
                "CLIENTE E",
            ],
            "Indirizzo completo": [
                "VIA ROMA 1",
                "VIA MILANO 2",
                "VIA TORINO 3",
                "VIA GENOVA 4",
                "VIA VENEZIA 5",
            ],
            "CAP": ["33100", "20100", "10100", "16100", "30100"],
            "Città": ["UDINE", "MILANO", "TORINO", "GENOVA", "VENEZIA"],
            "Regione": [
                "Friuli-Venezia Giulia",
                "Lombardia",
                "Piemonte",
                "Liguria",
                "Veneto",
            ],
            "Ore lavoro": [2.5, 3.0, 4.0, 2.0, 3.5],
            "Data visita di riferimento 2026": [
                "2026-03-15",
                "2026-04-20",
                "2026-05-10",
                "2026-06-15",
                "2026-07-20",
            ],
        }
    )


@pytest.fixture
def sample_ordini():
    """Sample confirmed orders for testing."""
    return pd.DataFrame(
        {
            "ID_Ordine": ["ORD001", "ORD002", "ORD003"],
            "Cliente": ["CLIENTE A", "CLIENTE B", "CLIENTE C"],
            "Indirizzo_Sede": ["VIA ROMA 1", "VIA MILANO 2", "VIA TORINO 3"],
            "Data_Ordine": ["2025-12-01", "2025-12-02", "2025-12-03"],
        }
    )


@pytest.fixture
def sample_planning():
    """Sample planning data for testing."""
    return pd.DataFrame(
        {
            "Settimana": [50, 50, 50],
            "Data": [
                datetime(2025, 12, 9),
                datetime(2025, 12, 10),
                datetime(2025, 12, 11),
            ],
            "Giorno": ["Lunedì", "Martedì", "Mercoledì"],
            "Ispettore": ["Adrian", "Salvatore", "Paolo"],
            "Tour_Zona": ["Cluster_1_Adrian", "Cluster_2_Salvatore", "Cluster_3_Paolo"],
            "Nome del Cliente": ["CLIENTE A", "CLIENTE B", "CLIENTE C"],
            "Città": ["UDINE", "UDINE", "MILANO"],
            "Regione": ["Friuli-Venezia Giulia", "Friuli-Venezia Giulia", "Lombardia"],
            "Ore lavoro": [2.5, 3.0, 4.0],
            "km_from_previous": [50, 30, 100],
            "Stato": ["Da Confermare", "Confermato", "Da Confermare"],
            "Note": ["", "", ""],
        }
    )


@pytest.fixture
def sample_vacations():
    """Sample vacation data for testing."""
    return pd.DataFrame(
        {
            "Ispettore": ["Salvatore", "Paolo"],
            "Data_Inizio": [datetime(2025, 12, 20), datetime(2025, 12, 24)],
            "Data_Fine": [datetime(2025, 12, 27), datetime(2025, 12, 26)],
            "Tipo": ["Ferie", "Ferie"],
            "Note": ["", ""],
        }
    )


@pytest.fixture
def sample_coordinates():
    """Sample geographic coordinates for testing."""
    return {
        "udine": (46.08, 13.18),
        "milano": (45.46, 9.19),
        "torino": (45.07, 7.69),
        "genova": (44.41, 8.93),
        "venezia": (45.44, 12.32),
    }
