# MODULBLOK PLANNING SYSTEM - TASK TRACKER

## 🎯 PROJECT GOAL
Build a web-based inspection visit planning system for Modulblok SPA with route optimization, Gantt calendar visualization, and inspector assignment management.

---

## 📅 TASKS

### ✅ Phase 0: Project Setup (2025-12-07)
- [x] Create PLANNING.md with architecture documentation
- [x] Create TASK.md for task tracking
- [ ] Set up folder structure (data/, tests/, templates/)
- [ ] Create requirements.txt with all dependencies
- [ ] Create .gitignore for data files

### 🔄 Phase 1: Core Engine (In Progress)
- [ ] Implement config.py with inspector configurations and constants
- [ ] Implement utils.py with helper functions:
  - [ ] normalize_string() for robust text matching
  - [ ] calculate_distance() for geodesic distances
  - [ ] is_available() for holiday/vacation checks
  - [ ] generate_email() for email templates
  - [ ] export_excel() for Excel formatting
- [ ] Implement planner_engine.py with core logic:
  - [ ] match_orders() - match ordini ↔ anagrafica
  - [ ] geocode_addresses() - get lat/lon coordinates
  - [ ] cluster_geographic() - K-means clustering
  - [ ] tsp_nearest_neighbor() - route optimization
  - [ ] assign_inspectors() - respect Paolo constraint
  - [ ] schedule_daily() - 8h/day, skip weekends
  - [ ] generate_planning() - orchestrate all steps
  - [ ] generate_renewals_list() - customers expiring in 90 days

### 🔄 Phase 2: Streamlit Web App
- [ ] Create app.py main structure with multi-page layout
- [ ] Implement Page 1: 🏠 Home (Generate Planning)
  - [ ] Upload Excel files (2 file uploaders)
  - [ ] Validate file structure
  - [ ] Generate Planning button
  - [ ] Progress bars for geocoding
  - [ ] Success/error messages
- [ ] Implement Page 2: 📅 Gantt Calendar
  - [ ] Create weekly Gantt chart with Plotly
  - [ ] Color-code by inspector
  - [ ] Add filters (inspector, zone, status)
  - [ ] Interactive hover details
  - [ ] Click to edit functionality
- [ ] Implement Page 3: ✏️ Assign Inspectors
  - [ ] Visit selection dropdown
  - [ ] Inspector reassignment with Paolo constraint validation
  - [ ] Status change (Confirmed/Pending/Cancelled)
  - [ ] Notes field
  - [ ] Save changes to session state
- [ ] Implement Page 4: 🏖️ Holidays & Vacations
  - [ ] Tab 1: National holidays list
  - [ ] Tab 2: Inspector vacations
  - [ ] Add/remove entries
  - [ ] Date validation
- [ ] Implement Page 5: 📧 Email Generator
  - [ ] Filter visits (DA_CONFERMARE status)
  - [ ] Multi-select checkbox list
  - [ ] Email template with placeholders
  - [ ] Generate emails button
  - [ ] Copy to clipboard functionality
- [ ] Implement Page 6: 📊 Statistics
  - [ ] KPI cards (visits, km, hours, days)
  - [ ] Chart: Visits per inspector (bar chart)
  - [ ] Chart: Tours by zone (pie chart)
  - [ ] Detailed breakdown table

### 🔄 Phase 3: Testing
- [ ] Create test_planner_engine.py:
  - [ ] test_match_orders_exact()
  - [ ] test_match_orders_whitespace()
  - [ ] test_match_orders_case_insensitive()
  - [ ] test_paolo_constraint_enforcement()
  - [ ] test_tsp_optimization()
  - [ ] test_weekend_skip()
  - [ ] test_daily_schedule_8h_limit()
- [ ] Create test_utils.py:
  - [ ] test_normalize_string()
  - [ ] test_calculate_distance()
  - [ ] test_is_available_weekend()
  - [ ] test_is_available_holiday()
  - [ ] test_is_available_vacation()
- [ ] Create conftest.py with test fixtures
- [ ] Run all tests with pytest
- [ ] Fix any failing tests

### 🔄 Phase 4: Documentation & Templates
- [ ] Create README.md with:
  - [ ] Installation instructions
  - [ ] Usage guide
  - [ ] Excel file format requirements
  - [ ] Troubleshooting section
  - [ ] Screenshots of UI
- [ ] Create data/templates/Anagrafica_Template.xlsx
- [ ] Create data/templates/Ordini_Template.xlsx
- [ ] Create example files with sample data
- [ ] Add inline code comments
- [ ] Add docstrings to all functions

### 🔄 Phase 5: Integration & Polish
- [ ] End-to-end test with real data
- [ ] Performance optimization for geocoding
- [ ] UI/UX polish (spacing, alignment, icons)
- [ ] Error handling improvements
- [ ] Edge case testing
- [ ] Final validation against success criteria

---

## 🚨 CRITICAL VALIDATIONS

Must verify before considering complete:

1. **Paolo Constraint:**
   - [ ] Cannot assign Paolo to regions outside [Lombardia, Piemonte, Liguria, Valle d'Aosta]
   - [ ] Warning shown if assigning others to Paolo's regions
   - [ ] Validation works in both automatic and manual assignment

2. **Order Matching:**
   - [ ] Exact matches work
   - [ ] Whitespace variations handled
   - [ ] Case-insensitive matching
   - [ ] Unmatched orders reported to user

3. **Schedule Constraints:**
   - [ ] No weekend dates
   - [ ] Max 8h/day including travel
   - [ ] Proper handling of week transitions

4. **Geocoding:**
   - [ ] Progress bar shows during geocoding
   - [ ] Fallback works for failed geocodes
   - [ ] Rate limiting respected (1 req/sec)

5. **Excel Export:**
   - [ ] All required sheets present
   - [ ] Correct column names
   - [ ] Proper date formatting
   - [ ] File downloads successfully

---

## 🐛 KNOWN ISSUES

_(Track bugs discovered during development)_

### Discovered During Work

_(Add new tasks/issues found during implementation)_

---

## 📊 PROGRESS TRACKER

- **Phase 0:** 40% (2/5 tasks)
- **Phase 1:** 0% (0/15 tasks)
- **Phase 2:** 0% (0/25 tasks)
- **Phase 3:** 0% (0/12 tasks)
- **Phase 4:** 0% (0/9 tasks)
- **Phase 5:** 0% (0/6 tasks)

**Overall Progress:** 3% (2/72 tasks)

---

## 🎯 NEXT STEPS

1. Set up folder structure
2. Create requirements.txt
3. Implement config.py
4. Implement utils.py
5. Implement planner_engine.py
6. Create Streamlit app skeleton
7. Implement each page one by one
8. Add tests
9. Create documentation

---

**Last Updated:** 2025-12-07
**Current Status:** Phase 0 - Project Setup
