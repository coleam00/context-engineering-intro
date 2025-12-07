"""
Configuration file for Modulblok Inspection Planning System.

Contains all constants, inspector configurations, and system parameters.
"""

from typing import Dict, List, Tuple

# ============================================================================
# INSPECTORS CONFIGURATION
# ============================================================================

INSPECTORS: Dict[str, Dict[str, any]] = {
    "Adrian": {
        "base_location": "Pagnacco, UD",
        "base_coords": (46.08, 13.18),
        "coverage": "national",
        "restricted_regions": [],
    },
    "Salvatore": {
        "base_location": "Pagnacco, UD",
        "base_coords": (46.08, 13.18),
        "coverage": "national",
        "restricted_regions": [],
    },
    "Mattia": {
        "base_location": "Pagnacco, UD",
        "base_coords": (46.08, 13.18),
        "coverage": "national",
        "restricted_regions": [],
    },
    "Paolo": {
        "base_location": "Milano",
        "base_coords": (45.46, 9.19),
        "coverage": "regional",
        "allowed_regions": ["Lombardia", "Piemonte", "Liguria", "Valle d'Aosta"],
    },
}

# Paolo's allowed regions (CRITICAL CONSTRAINT)
PAOLO_REGIONS: List[str] = ["Lombardia", "Piemonte", "Liguria", "Valle d'Aosta"]

# All inspectors list
ALL_INSPECTORS: List[str] = ["Adrian", "Salvatore", "Mattia", "Paolo"]

# National coverage inspectors (excluding Paolo)
NATIONAL_INSPECTORS: List[str] = ["Adrian", "Salvatore", "Mattia"]

# ============================================================================
# WORK PARAMETERS
# ============================================================================

WORK_PARAMS: Dict[str, any] = {
    # Working hours
    "max_hours_per_day": 8.0,
    "max_hours_friday": 6.5,  # Must return by 17:30
    "buffer_hours_per_visit": 0.5,  # Buffer for unexpected issues

    # Travel parameters
    "average_speed_kmh": 70,  # Average travel speed
    "max_daily_km": 400,  # Soft limit for daily travel

    # Scheduling
    "work_days": [0, 1, 2, 3, 4],  # Monday=0, Friday=4
    "office_days_per_week": 2,  # Typical office days (flexible)

    # Clustering
    "default_clusters": 8,  # Number of geographic clusters
    "min_clients_per_cluster": 3,  # Minimum clients to form a cluster

    # Renewals
    "renewal_alert_days": 90,  # Alert for contracts expiring within 90 days
}

# ============================================================================
# COLORS & UI THEME
# ============================================================================

COLORS: Dict[str, any] = {
    # Inspector colors (for Gantt chart)
    "inspectors": {
        "Adrian": "#1f77b4",  # Blue
        "Salvatore": "#ff7f0e",  # Orange
        "Mattia": "#2ca02c",  # Green
        "Paolo": "#d62728",  # Red
    },

    # Status colors
    "status": {
        "confermato": "#28a745",  # Green
        "da_confermare": "#ffc107",  # Yellow
        "annullato": "#dc3545",  # Red
        "completato": "#17a2b8",  # Blue
    },

    # UI colors
    "primary": "#1f77b4",  # Blue
    "success": "#28a745",  # Green
    "warning": "#ffc107",  # Yellow
    "danger": "#dc3545",  # Red
    "info": "#17a2b8",  # Cyan
}

# ============================================================================
# EXCEL COLUMN MAPPINGS
# ============================================================================

# Anagrafica Clienti columns (expected input)
ANAGRAFICA_COLUMNS: Dict[str, str] = {
    "id_cliente": "ID Cliente",
    "nome_cliente": "Nome del Cliente",
    "indirizzo": "Indirizzo completo",
    "cap": "CAP",
    "citta": "Città",
    "regione": "Regione",
    "ore_lavoro": "Ore lavoro",
    "data_riferimento_2026": "Data visita di riferimento 2026",
}

# Ordini Confermati columns (expected input)
ORDINI_COLUMNS: Dict[str, str] = {
    "id_ordine": "ID_Ordine",
    "cliente": "Cliente",
    "indirizzo_sede": "Indirizzo_Sede",
    "data_ordine": "Data_Ordine",
}

# Planning output columns
PLANNING_COLUMNS: List[str] = [
    "Settimana",
    "Data",
    "Giorno",
    "Ispettore",
    "Tour_Zona",
    "Cliente",
    "Indirizzo",
    "Città",
    "Regione",
    "Ore_Stimate",
    "Km_da_Precedente",
    "Stato",
    "Note",
]

# Renewals list columns
RENEWALS_COLUMNS: List[str] = [
    "ID_Cliente",
    "Cliente",
    "Indirizzo",
    "Città",
    "Regione",
    "Data_Scadenza_2026",
    "Giorni_a_Scadenza",
    "Stato_Contatto",
    "Data_Contatto",
    "Ordine_Ricevuto",
    "Note",
]

# ============================================================================
# ITALIAN HOLIDAYS (2025-2026)
# ============================================================================

ITALIAN_HOLIDAYS: List[Tuple[str, str]] = [
    # 2025
    ("2025-01-01", "Capodanno"),
    ("2025-01-06", "Epifania"),
    ("2025-04-21", "Lunedì dell'Angelo (Pasquetta)"),
    ("2025-04-25", "Festa della Liberazione"),
    ("2025-05-01", "Festa dei Lavoratori"),
    ("2025-06-02", "Festa della Repubblica"),
    ("2025-08-15", "Ferragosto"),
    ("2025-11-01", "Tutti i Santi"),
    ("2025-12-08", "Immacolata Concezione"),
    ("2025-12-25", "Natale"),
    ("2025-12-26", "Santo Stefano"),

    # 2026
    ("2026-01-01", "Capodanno"),
    ("2026-01-06", "Epifania"),
    ("2026-04-06", "Lunedì dell'Angelo (Pasquetta)"),
    ("2026-04-25", "Festa della Liberazione"),
    ("2026-05-01", "Festa dei Lavoratori"),
    ("2026-06-02", "Festa della Repubblica"),
    ("2026-08-15", "Ferragosto"),
    ("2026-11-01", "Tutti i Santi"),
    ("2026-12-08", "Immacolata Concezione"),
    ("2026-12-25", "Natale"),
    ("2026-12-26", "Santo Stefano"),
]

# ============================================================================
# REGIONAL FALLBACK COORDINATES
# ============================================================================
# Used when geocoding fails for specific addresses

REGIONAL_COORDS: Dict[str, Tuple[float, float]] = {
    "Abruzzo": (42.35, 13.40),
    "Basilicata": (40.64, 15.80),
    "Calabria": (39.31, 16.25),
    "Campania": (40.83, 14.25),
    "Emilia-Romagna": (44.49, 11.34),
    "Friuli-Venezia Giulia": (45.64, 13.78),
    "Lazio": (41.90, 12.50),
    "Liguria": (44.41, 8.93),
    "Lombardia": (45.46, 9.19),
    "Marche": (43.62, 13.52),
    "Molise": (41.56, 14.66),
    "Piemonte": (45.07, 7.69),
    "Puglia": (41.13, 16.87),
    "Sardegna": (40.12, 9.01),
    "Sicilia": (38.12, 13.36),
    "Toscana": (43.77, 11.25),
    "Trentino-Alto Adige": (46.07, 11.12),
    "Umbria": (43.11, 12.39),
    "Valle d'Aosta": (45.74, 7.43),
    "Veneto": (45.44, 12.32),
}

# ============================================================================
# EMAIL TEMPLATES
# ============================================================================

EMAIL_TEMPLATE: str = """Gentile {cliente},

Le proponiamo una visita ispettiva per la manutenzione delle scaffalature presso la Vostra sede:

📅 Data proposta: {data}
📍 Sede: {indirizzo}, {citta}
⏱️ Durata stimata: {ore} ore
👤 Ispettore: {ispettore}

La preghiamo di confermare la disponibilità per la data indicata.

Cordiali saluti,
Modulblok SPA - Area SERVICE
"""

# ============================================================================
# GEOCODING SETTINGS
# ============================================================================

GEOCODING: Dict[str, any] = {
    "user_agent": "modulblok_planning_v1",
    "timeout": 10,  # seconds
    "rate_limit": 1.0,  # seconds between requests (Nominatim requires 1 req/sec)
    "country": "Italia",
    "cache_results": True,
}

# ============================================================================
# VALIDATION RULES
# ============================================================================

VALIDATION: Dict[str, any] = {
    "min_ore_lavoro": 0.5,  # Minimum hours for a visit
    "max_ore_lavoro": 12.0,  # Maximum hours for a visit
    "min_distance_km": 0,  # Minimum distance between clients
    "max_distance_km": 1000,  # Maximum distance in a single day
}

# ============================================================================
# FILE PATHS
# ============================================================================

PATHS: Dict[str, str] = {
    "data_dir": "data",
    "templates_dir": "data/templates",
    "output_dir": "data/output",
    "tests_dir": "tests",
}

# ============================================================================
# UI ICONS
# ============================================================================

ICONS: Dict[str, str] = {
    "home": "🏠",
    "calendar": "📅",
    "edit": "✏️",
    "vacation": "🏖️",
    "email": "📧",
    "stats": "📊",
    "visit": "📍",
    "confirmed": "✅",
    "pending": "🟡",
    "cancelled": "🔴",
    "km": "🚗",
    "time": "⏱️",
    "person": "👤",
    "location": "📍",
    "warning": "⚠️",
    "success": "✅",
    "error": "❌",
    "info": "ℹ️",
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def validate_inspector_assignment(inspector: str, region: str) -> Tuple[bool, str]:
    """
    Validate if an inspector can be assigned to a specific region.

    Args:
        inspector: Inspector name
        region: Region name

    Returns:
        Tuple of (is_valid, message)

    Example:
        >>> validate_inspector_assignment("Paolo", "Toscana")
        (False, "Paolo può lavorare solo in: Lombardia, Piemonte, Liguria, Valle d'Aosta")
    """
    if inspector == "Paolo" and region not in PAOLO_REGIONS:
        return False, f"Paolo può lavorare solo in: {', '.join(PAOLO_REGIONS)}"

    if inspector != "Paolo" and region in PAOLO_REGIONS:
        return True, f"⚠️ Attenzione: {region} è zona di competenza di Paolo"

    return True, ""


def get_available_inspectors(region: str) -> List[str]:
    """
    Get list of inspectors available for a specific region.

    Args:
        region: Region name

    Returns:
        List of available inspector names

    Example:
        >>> get_available_inspectors("Lombardia")
        ["Paolo"]
        >>> get_available_inspectors("Toscana")
        ["Adrian", "Salvatore", "Mattia"]
    """
    if region in PAOLO_REGIONS:
        return ["Paolo"]
    else:
        return NATIONAL_INSPECTORS.copy()


def get_inspector_color(inspector: str) -> str:
    """
    Get the color code for an inspector.

    Args:
        inspector: Inspector name

    Returns:
        Hex color code
    """
    return COLORS["inspectors"].get(inspector, "#666666")


def get_status_color(status: str) -> str:
    """
    Get the color code for a status.

    Args:
        status: Status name

    Returns:
        Hex color code
    """
    status_lower = status.lower().replace(" ", "_")
    return COLORS["status"].get(status_lower, "#666666")
