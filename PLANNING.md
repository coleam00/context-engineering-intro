# MODULBLOK INSPECTION PLANNING SYSTEM - PLANNING DOCUMENT

## 🎯 PROJECT OVERVIEW

**Project Name:** Modulblok Inspection Planning System
**Client:** Modulblok SPA - Area SERVICE
**Purpose:** Web-based system for optimizing and managing inspection visit schedules
**Technology Stack:** Python + Streamlit + Plotly + Geopy + scikit-learn

## 👥 BUSINESS CONTEXT

### Team Structure
- **4 Inspectors:**
  - Adrian (base: Pagnacco, UD) - National coverage
  - Salvatore (base: Pagnacco, UD) - National coverage
  - Mattia (base: Pagnacco, UD) - National coverage
  - Paolo (base: Milano) - **RESTRICTED** to Lombardia, Piemonte, Liguria, Valle d'Aosta

### Critical Business Rule: Paolo's Restriction
**This is the most important constraint in the entire system:**
- Paolo can ONLY work in: Lombardia, Piemonte, Liguria, Valle d'Aosta
- Other inspectors can work anywhere EXCEPT these regions should preferably go to Paolo
- System must enforce this at all levels (assignment, modification, validation)

## 🏗️ ARCHITECTURE

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit Web UI                     │
├─────────────────────────────────────────────────────────┤
│  Home  │  Gantt  │  Assign  │  Holidays  │  Email  │  Stats  │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│              planner_engine.py (Core Logic)             │
├─────────────────────────────────────────────────────────┤
│  • Excel Import/Export                                  │
│  • Order Matching (ordini ↔ anagrafica)                │
│  • Geocoding (Geopy + Nominatim)                        │
│  • Geographic Clustering (K-means)                      │
│  • TSP Optimization (Nearest Neighbor Heuristic)        │
│  • Daily Scheduling (8h limit, no weekends)             │
│  • Inspector Assignment (Paolo constraint)              │
└─────────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│                  utils.py (Helpers)                     │
├─────────────────────────────────────────────────────────┤
│  • Distance calculations                                │
│  • Availability checks (holidays, vacations)            │
│  • Email template generation                            │
│  • Data normalization                                   │
└─────────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│                  config.py (Settings)                   │
├─────────────────────────────────────────────────────────┤
│  • Inspectors configuration                             │
│  • Regional constraints                                 │
│  • Work parameters (hours, speed, etc.)                 │
│  • Color schemes                                        │
└─────────────────────────────────────────────────────────┘
```

### File Structure

```
modulblok_planning/
│
├── app.py                          # Main Streamlit application
│   ├── Page 1: 🏠 Home (Generate Planning)
│   ├── Page 2: 📅 Gantt Calendar (Main View)
│   ├── Page 3: ✏️ Assign Inspectors
│   ├── Page 4: 🏖️ Holidays & Vacations
│   ├── Page 5: 📧 Email Generator
│   └── Page 6: 📊 Statistics
│
├── planner_engine.py               # Core optimization logic
│   ├── match_orders()              # Match ordini ↔ anagrafica
│   ├── geocode_addresses()         # Get coordinates
│   ├── cluster_geographic()        # K-means clustering
│   ├── tsp_nearest_neighbor()      # Route optimization
│   ├── assign_inspectors()         # Respect Paolo constraint
│   ├── schedule_daily()            # 8h/day, no weekends
│   └── generate_planning()         # Orchestrate all steps
│
├── utils.py                        # Utility functions
│   ├── normalize_string()          # Clean text for matching
│   ├── calculate_distance()        # Geodesic distance
│   ├── is_available()              # Check holidays/vacations
│   ├── generate_email()            # Email templates
│   └── export_excel()              # Excel formatting
│
├── config.py                       # Configuration
│   ├── INSPECTORS dict             # Inspector info
│   ├── PAOLO_REGIONS list          # Paolo's allowed regions
│   ├── WORK_PARAMS dict            # Hours, speed, etc.
│   └── COLORS dict                 # UI color scheme
│
├── requirements.txt                # Python dependencies
├── README.md                       # Setup & usage docs
├── .gitignore                      # Git exclusions
│
├── data/                           # Data folder (gitignored)
│   ├── templates/
│   │   ├── Anagrafica_Template.xlsx
│   │   └── Ordini_Template.xlsx
│   └── output/
│       ├── Lista_Rinnovi_YYYYMMDD.xlsx
│       └── Planning_Ispettori_YYYYMMDD.xlsx
│
└── tests/                          # Unit tests
    ├── test_planner_engine.py
    ├── test_utils.py
    └── conftest.py
```

## 🔄 DATA FLOW

### Input Files

**1. Anagrafica_Clienti.xlsx** (Customer Master Data)
- Columns: ID_Cliente, Nome del cliente, Indirizzo completo, CAP, Città, Regione, Ore lavoro, Data riferimento 2026

**2. Ordini_Confermati.xlsx** (Confirmed Orders)
- Columns: ID_Ordine, Cliente, Indirizzo_Sede, Data_Ordine

### Processing Pipeline

```
1. UPLOAD
   ├─ User uploads 2 Excel files
   └─ Validate column structure

2. MATCH
   ├─ Normalize strings (uppercase, trim, collapse whitespace)
   ├─ Inner join on (Cliente, Indirizzo)
   ├─ Only matched orders proceed
   └─ Report unmatched for debugging

3. GEOCODE
   ├─ Use Geopy + Nominatim (OpenStreetMap)
   ├─ Input: CAP + Città + "Italia"
   ├─ Fallback: Regional coordinates
   └─ Show progress bar (2-3 min for 100 addresses)

4. CLUSTER
   ├─ K-means on (lat, lon)
   ├─ Default: 8 clusters
   └─ Group by geographic zones

5. ASSIGN
   ├─ If region in [Lombardia, Piemonte, Liguria, Valle d'Aosta]:
   │   └─ Assign to Paolo
   ├─ Else:
   │   └─ Random choice [Adrian, Salvatore, Mattia]

6. OPTIMIZE TSP
   ├─ For each cluster:
   │   ├─ Order by geographic proximity
   │   ├─ First = closest to base
   │   └─ Next = always closest to previous
   └─ Create weekly tours

7. SCHEDULE
   ├─ Respect constraints:
   │   ├─ 8h/day max
   │   ├─ No weekends
   │   ├─ Buffer: +0.5h per visit
   │   └─ Friday return by 17:30
   └─ Assign dates

8. OUTPUT
   ├─ Lista_Rinnovi_YYYYMMDD.xlsx (renewals)
   └─ Planning_Ispettori_YYYYMMDD.xlsx (full planning)
```

### Output Files

**1. Lista_Rinnovi_YYYYMMDD.xlsx**
- Customers with contracts expiring within 90 days
- Columns for tracking contact status

**2. Planning_Ispettori_YYYYMMDD.xlsx**
- Sheet 1: Complete planning with all tours
- Sheets 2-5: Individual inspector views
- Sheet 6: KPIs and statistics

## 🎨 UI/UX DESIGN

### Color Scheme

```python
COLORS = {
    'inspectors': {
        'Adrian': '#1f77b4',      # Blue
        'Salvatore': '#ff7f0e',   # Orange
        'Mattia': '#2ca02c',      # Green
        'Paolo': '#d62728'        # Red
    },
    'status': {
        'confirmed': '#28a745',    # Green
        'pending': '#ffc107',      # Yellow
        'cancelled': '#dc3545'     # Red
    }
}
```

### Page-by-Page Functionality

**Page 1: 🏠 Home**
- Upload 2 Excel files
- Click "Generate Planning" → runs full pipeline
- Progress indicators for slow operations
- Save result to `st.session_state.planning`

**Page 2: 📅 Gantt Calendar** (Main View)
- Weekly Gantt chart using Plotly
- Color-coded by inspector
- Filters: inspector, zone, status
- Click block → edit details

**Page 3: ✏️ Assign Inspectors**
- Select visit from dropdown
- Change inspector (respecting Paolo constraint)
- Modify status, add notes
- Save changes

**Page 4: 🏖️ Holidays & Vacations**
- Tab 1: National holidays calendar
- Tab 2: Inspector vacations/absences
- Add/remove entries
- Validation during scheduling

**Page 5: 📧 Email Generator**
- Select visits to confirm
- Generate email templates
- Copy to clipboard
- Track sent status

**Page 6: 📊 Statistics**
- KPI cards (total visits, km, hours)
- Charts (visits per inspector, tours by zone)
- Detailed breakdown table

## ⚙️ ALGORITHMS

### 1. String Matching (Order ↔ Master Data)

```python
def normalize_string(text: str) -> str:
    """Normalize for robust matching."""
    return text.upper().strip().replace('  ', ' ')

# Match on (Cliente, Indirizzo) with normalization
```

### 2. Geocoding

```python
# Using Nominatim (free, no API key)
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="modulblok_planning")
location = geolocator.geocode(f"{cap} {citta}, Italia")

if location:
    return (location.latitude, location.longitude)
else:
    # Fallback to regional coordinates
    return get_regional_coords(regione)
```

### 3. K-means Clustering

```python
from sklearn.cluster import KMeans

# Cluster customers by location
kmeans = KMeans(n_clusters=8, random_state=42)
cluster_labels = kmeans.fit_predict(coords)
```

### 4. TSP Nearest Neighbor Heuristic

```python
def tsp_nearest_neighbor(clients: pd.DataFrame, base_coords: tuple) -> pd.DataFrame:
    """
    Optimize tour using nearest neighbor algorithm.

    Args:
        clients: DataFrame with lat, lon columns
        base_coords: (lat, lon) of base location

    Returns:
        DataFrame sorted by tour order
    """
    unvisited = clients.copy()
    tour = []
    current = base_coords

    while len(unvisited) > 0:
        # Find closest unvisited client
        distances = unvisited.apply(
            lambda row: geodesic(current, (row['lat'], row['lon'])).km,
            axis=1
        )
        nearest_idx = distances.idxmin()
        nearest = unvisited.loc[nearest_idx]

        tour.append(nearest)
        current = (nearest['lat'], nearest['lon'])
        unvisited = unvisited.drop(nearest_idx)

    return pd.DataFrame(tour)
```

### 5. Daily Scheduling

```python
def schedule_daily(clients_ordered: pd.DataFrame, inspector: str) -> pd.DataFrame:
    """
    Assign dates respecting constraints.

    Constraints:
    - Max 8h/day (including travel time)
    - No weekends
    - Friday return by 17:30
    - Buffer: +0.5h per visit

    Args:
        clients_ordered: Clients sorted by TSP
        inspector: Inspector name

    Returns:
        DataFrame with assigned dates
    """
    current_date = datetime.now()
    daily_hours = 0
    results = []

    for _, client in clients_ordered.iterrows():
        # Skip weekends
        while current_date.weekday() >= 5:
            current_date += timedelta(days=1)

        # Calculate hours needed
        visit_hours = client['ore_lavoro'] + 0.5  # Buffer
        travel_hours = calculate_travel_time(...)
        total_hours = visit_hours + travel_hours

        # Check if fits in current day
        if daily_hours + total_hours > 8:
            # Move to next day
            current_date += timedelta(days=1)
            daily_hours = 0

        # Assign visit
        client['data_visita'] = current_date
        daily_hours += total_hours
        results.append(client)

    return pd.DataFrame(results)
```

## 🚨 CRITICAL CONSTRAINTS

### 1. Paolo's Regional Restriction

**Implementation:**
- Validate in assignment function
- Validate in UI when manually changing
- Show warning if user tries to assign Paolo elsewhere
- Show warning if assigning others to Paolo's regions

```python
PAOLO_REGIONS = ['Lombardia', 'Piemonte', 'Liguria', "Valle d'Aosta"]

def validate_assignment(inspector: str, region: str) -> tuple[bool, str]:
    if inspector == 'Paolo' and region not in PAOLO_REGIONS:
        return False, f"Paolo can only work in {', '.join(PAOLO_REGIONS)}"
    return True, ""
```

### 2. Robust Order Matching

- Normalize all strings before comparison
- Report unmatched orders for manual review
- Only plan visits with confirmed orders

### 3. Geocoding Rate Limits

- Nominatim: 1 request/second
- Always add `time.sleep(1)` between requests
- Show progress bar (this is slow!)
- Cache results to avoid re-geocoding

### 4. Work Constraints

- 8 hours/day maximum
- No work on weekends
- Buffer time for unexpected issues (+0.5h per visit)
- Friday return constraint (home by 17:30)

## 📊 VALIDATION & TESTING

### Unit Tests Required

1. **test_planner_engine.py**
   - Test order matching (exact match, whitespace differences, case differences)
   - Test geocoding fallback
   - Test TSP optimization logic
   - Test Paolo constraint enforcement

2. **test_utils.py**
   - Test string normalization
   - Test distance calculations
   - Test availability checks

### Integration Tests

1. Upload valid Excel files → successful planning
2. Upload with unmatched orders → report shown
3. Assign Paolo to wrong region → validation error
4. Schedule crossing weekend → dates skip correctly

### Manual Testing Checklist

- [ ] Upload 2 Excel files
- [ ] See progress bar during geocoding
- [ ] Planning generated successfully
- [ ] Gantt chart displays correctly
- [ ] Can modify inspector assignments
- [ ] Paolo constraint enforced
- [ ] Weekend dates skipped
- [ ] Export Excel works
- [ ] Email generation works
- [ ] Statistics calculated correctly

## 🔐 SECURITY & PRIVACY

### Data Handling

- Excel files contain sensitive customer data
- Must be gitignored
- No data persisted to disk (except user exports)
- Use `st.session_state` for in-memory storage

### .gitignore

```
data/
*.xlsx
*.xls
!data/templates/*.xlsx
.env
__pycache__/
*.pyc
.pytest_cache/
```

## 📈 PERFORMANCE CONSIDERATIONS

### Slow Operations

1. **Geocoding** (2-3 min for 100 addresses)
   - Show progress bar
   - Cache results in session state
   - Consider pre-geocoding common addresses

2. **TSP Optimization** (fast for <100 clients per cluster)
   - Nearest neighbor is O(n²) but acceptable
   - For >200 clients, consider better algorithms

### Optimization Opportunities (Future)

- Cache geocoding results in database
- Use Google Maps API for real distances
- Implement better TSP solver (OR-Tools)
- Add background job processing

## 🚀 DEPLOYMENT

### Local Development

```bash
python -m venv venv_linux
source venv_linux/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Production (Future)

- Streamlit Cloud
- Docker container
- Environment variables for configuration

## 📝 CONVENTIONS

### Naming

- Files: `snake_case.py`
- Functions: `snake_case()`
- Classes: `PascalCase`
- Constants: `UPPER_CASE`
- Session state keys: `snake_case`

### Code Style

- PEP8 compliant
- Type hints for all functions
- Google-style docstrings
- Comments for complex logic

### Git Commits

- Format: `feat: description` or `fix: description`
- Be specific about what changed
- Reference issue numbers if applicable

## 🎯 SUCCESS CRITERIA

The system is complete when:

1. ✅ Can upload 2 Excel files
2. ✅ Matches orders to customer master data
3. ✅ Geocodes all addresses with progress indication
4. ✅ Generates optimized tours using TSP
5. ✅ Enforces Paolo's regional constraint
6. ✅ Creates weekly Gantt chart visualization
7. ✅ Allows manual inspector assignment
8. ✅ Respects holidays and vacations
9. ✅ Generates email templates
10. ✅ Exports complete planning to Excel
11. ✅ Shows meaningful statistics
12. ✅ Passes all unit tests

## 🔄 FUTURE ENHANCEMENTS (Not Now)

Phase 2 could include:
- Google Maps API for real distances
- Email SMTP integration
- PDF export with branding
- Multi-user authentication
- Database backend
- Mobile responsive design
- Machine learning for time predictions

---

**Last Updated:** 2025-12-07
**Status:** Ready for implementation
