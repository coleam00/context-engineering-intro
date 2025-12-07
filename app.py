"""
Modulblok Inspection Planning System - Streamlit Web Application

Multi-page application for managing and optimizing inspection visit schedules.
"""

import os
from datetime import datetime
from typing import Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from config import (
    ALL_INSPECTORS,
    COLORS,
    ICONS,
    PATHS,
    validate_inspector_assignment,
    get_available_inspectors,
    get_inspector_color,
)
from planner_engine import (
    generate_planning,
    update_inspector_assignment,
)
from utils import (
    validate_anagrafica_columns,
    validate_ordini_columns,
    format_planning_excel,
    format_renewals_excel,
    calculate_kpis,
    get_visits_by_inspector,
    get_visits_by_region,
    generate_bulk_emails,
    format_duration,
    format_distance,
)


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Modulblok Planning",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if "planning" not in st.session_state:
    st.session_state.planning = None

if "renewals" not in st.session_state:
    st.session_state.renewals = None

if "unmatched_orders" not in st.session_state:
    st.session_state.unmatched_orders = None

if "stats" not in st.session_state:
    st.session_state.stats = {}

if "vacations" not in st.session_state:
    st.session_state.vacations = pd.DataFrame(
        columns=["Ispettore", "Data_Inizio", "Data_Fine", "Tipo", "Note"]
    )

if "custom_holidays" not in st.session_state:
    st.session_state.custom_holidays = pd.DataFrame(columns=["Data", "Nome"])


# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

def render_sidebar():
    """Render sidebar with navigation and stats."""
    with st.sidebar:
        st.title(f"{ICONS['km']} Modulblok Planning")
        st.markdown("---")

        # Navigation menu
        st.subheader("Menu")
        page = st.radio(
            "Seleziona pagina:",
            [
                f"{ICONS['home']} Home",
                f"{ICONS['calendar']} Gantt Calendario",
                f"{ICONS['edit']} Assegna Ispettori",
                f"{ICONS['vacation']} Ferie & Festività",
                f"{ICONS['email']} Email Clienti",
                f"{ICONS['stats']} Statistiche",
            ],
            label_visibility="collapsed",
        )

        st.markdown("---")

        # Quick stats
        if st.session_state.planning is not None:
            st.subheader("Quick Stats")
            planning_df = st.session_state.planning

            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    f"{ICONS['visit']} Visite",
                    len(planning_df),
                )
            with col2:
                confirmed = len(
                    planning_df[planning_df.get("Stato", "") == "Confermato"]
                )
                st.metric(f"{ICONS['confirmed']} Confermate", confirmed)

        st.markdown("---")
        st.caption("Modulblok SPA © 2025")

    return page


# ============================================================================
# PAGE 1: HOME - GENERATE PLANNING
# ============================================================================

def page_home():
    """Home page: Upload files and generate planning."""
    st.title(f"{ICONS['home']} Genera Planning Ottimizzato")
    st.markdown(
        "Carica i file Excel per generare automaticamente il planning delle visite ispettive."
    )

    # Upload section
    st.markdown("### 📤 Upload File Excel")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 1️⃣ Anagrafica Clienti")
        anagrafica_file = st.file_uploader(
            "Upload Anagrafica_Clienti.xlsx",
            type=["xlsx", "xls"],
            key="anagrafica",
        )

        if anagrafica_file:
            anagrafica_df = pd.read_excel(anagrafica_file)
            is_valid, missing = validate_anagrafica_columns(anagrafica_df)

            if is_valid:
                st.success(f"{ICONS['success']} {len(anagrafica_df)} clienti caricati")
            else:
                st.error(
                    f"{ICONS['error']} Colonne mancanti: {', '.join(missing)}"
                )
        else:
            anagrafica_df = None

    with col2:
        st.markdown("#### 2️⃣ Ordini Confermati")
        ordini_file = st.file_uploader(
            "Upload Ordini_Confermati.xlsx",
            type=["xlsx", "xls"],
            key="ordini",
        )

        if ordini_file:
            ordini_df = pd.read_excel(ordini_file)
            is_valid, missing = validate_ordini_columns(ordini_df)

            if is_valid:
                st.success(f"{ICONS['success']} {len(ordini_df)} ordini caricati")
            else:
                st.error(
                    f"{ICONS['error']} Colonne mancanti: {', '.join(missing)}"
                )
        else:
            ordini_df = None

    st.markdown("---")

    # Generate planning button
    if anagrafica_df is not None and ordini_df is not None:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(
                "🚀 GENERA PLANNING CON TSP OTTIMIZZATO",
                use_container_width=True,
                type="primary",
            ):
                generate_planning_workflow(anagrafica_df, ordini_df)
    else:
        st.warning(
            f"{ICONS['warning']} Carica entrambi i file per generare il planning"
        )


def generate_planning_workflow(anagrafica_df: pd.DataFrame, ordini_df: pd.DataFrame):
    """Execute planning generation workflow with progress indicators."""
    progress_container = st.container()

    with progress_container:
        progress_bar = st.progress(0)
        status_text = st.empty()

        def progress_callback(step, message):
            progress = step / 6
            progress_bar.progress(progress)
            status_text.text(message)

        try:
            # Generate planning
            result = generate_planning(
                anagrafica_df,
                ordini_df,
                progress_callback=progress_callback,
            )

            # Store in session state
            st.session_state.planning = result["planning"]
            st.session_state.renewals = result["renewals"]
            st.session_state.unmatched_orders = result["unmatched_orders"]
            st.session_state.stats = result["stats"]

            # Add default status and notes columns
            st.session_state.planning["Stato"] = "Da Confermare"
            st.session_state.planning["Note"] = ""

            # Complete
            progress_bar.progress(1.0)
            status_text.empty()

            # Success message
            st.success(
                f"{ICONS['success']} Planning generato con successo!\n\n"
                f"- {result['stats']['visite_pianificate']} visite pianificate\n"
                f"- {result['stats']['settimane_necessarie']} settimane necessarie\n"
                f"- {result['stats']['km_totali']:.0f} km totali"
            )

            # Show unmatched orders if any
            if len(result["unmatched_orders"]) > 0:
                st.warning(
                    f"{ICONS['warning']} {len(result['unmatched_orders'])} ordini NON matchati"
                )
                with st.expander("Mostra ordini non matchati"):
                    st.dataframe(result["unmatched_orders"])

        except Exception as e:
            st.error(f"{ICONS['error']} Errore durante la generazione: {str(e)}")
            import traceback

            st.code(traceback.format_exc())


# ============================================================================
# PAGE 2: GANTT CALENDAR
# ============================================================================

def page_gantt():
    """Gantt calendar view of planning."""
    st.title(f"{ICONS['calendar']} Gantt Calendario Settimanale")

    if st.session_state.planning is None or len(st.session_state.planning) == 0:
        st.warning(
            f"{ICONS['warning']} Nessun planning disponibile. Vai alla Home per generarlo."
        )
        return

    planning_df = st.session_state.planning.copy()

    # Filters
    st.markdown("### 🔍 Filtri")
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_inspectors = st.multiselect(
            "Ispettori",
            options=ALL_INSPECTORS,
            default=ALL_INSPECTORS,
        )

    with col2:
        regions = planning_df["Regione"].unique().tolist()
        selected_regions = st.multiselect(
            "Regioni",
            options=regions,
            default=regions,
        )

    with col3:
        statuses = planning_df["Stato"].unique().tolist()
        selected_statuses = st.multiselect(
            "Stati",
            options=statuses,
            default=statuses,
        )

    # Apply filters
    filtered_df = planning_df[
        (planning_df["Ispettore"].isin(selected_inspectors))
        & (planning_df["Regione"].isin(selected_regions))
        & (planning_df["Stato"].isin(selected_statuses))
    ]

    if len(filtered_df) == 0:
        st.warning("Nessuna visita corrisponde ai filtri selezionati")
        return

    st.markdown("---")

    # Create Gantt chart
    st.markdown("### 📊 Vista Gantt")
    render_gantt_chart(filtered_df)


def render_gantt_chart(df: pd.DataFrame):
    """Render Gantt chart using Plotly."""
    # Prepare data for Gantt
    df = df.copy()
    df["Data"] = pd.to_datetime(df["Data"])

    # Create end time (assuming each visit ends same day)
    df["Data_Fine"] = df["Data"] + pd.Timedelta(hours=8)

    # Create task label
    df["Task"] = df.apply(
        lambda row: f"{row['Nome del Cliente']} - {row['Città']}", axis=1
    )

    # Create color mapping
    df["Color"] = df["Ispettore"].apply(get_inspector_color)

    # Create Gantt chart
    fig = px.timeline(
        df,
        x_start="Data",
        x_end="Data_Fine",
        y="Ispettore",
        color="Ispettore",
        hover_data=["Nome del Cliente", "Città", "Ore lavoro", "km_from_previous"],
        title="Planning Visite Ispettive",
        color_discrete_map={
            inspector: get_inspector_color(inspector)
            for inspector in df["Ispettore"].unique()
        },
    )

    fig.update_layout(
        height=600,
        xaxis_title="Data",
        yaxis_title="Ispettore",
        showlegend=True,
    )

    st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# PAGE 3: ASSIGN INSPECTORS
# ============================================================================

def page_assign():
    """Assign/modify inspector assignments."""
    st.title(f"{ICONS['edit']} Assegna/Modifica Ispettori")

    if st.session_state.planning is None or len(st.session_state.planning) == 0:
        st.warning(
            f"{ICONS['warning']} Nessun planning disponibile. Vai alla Home per generarlo."
        )
        return

    planning_df = st.session_state.planning

    st.info(
        f"{ICONS['info']} Modifica l'assegnazione degli ispettori. "
        "Paolo può lavorare solo in Lombardia, Piemonte, Liguria, Valle d'Aosta."
    )

    # Visit selector
    st.markdown("### Seleziona Visita")

    visit_options = [
        f"{row['Data'].strftime('%d/%m')} - {row['Nome del Cliente']} - {row['Ispettore']}"
        for _, row in planning_df.iterrows()
    ]

    selected_visit_idx = st.selectbox(
        "Visita:",
        options=range(len(visit_options)),
        format_func=lambda i: visit_options[i],
    )

    if selected_visit_idx is not None:
        st.markdown("---")
        render_visit_editor(planning_df, selected_visit_idx)


def render_visit_editor(df: pd.DataFrame, visit_idx: int):
    """Render visit editor form."""
    visit = df.iloc[visit_idx]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 📍 Cliente")
        st.write(f"**{visit['Nome del Cliente']}**")
        st.write(f"{visit['Città']} ({visit['Regione']})")
        st.write(f"{visit['Indirizzo completo']}")

    with col2:
        st.markdown("#### 👤 Ispettore")

        # Get available inspectors for this region
        available_inspectors = get_available_inspectors(visit["Regione"])

        if len(available_inspectors) == 1:
            st.warning(
                f"{ICONS['warning']} {visit['Regione']} è zona di competenza Paolo"
            )

        new_inspector = st.selectbox(
            "Ispettore:",
            options=available_inspectors,
            index=available_inspectors.index(visit["Ispettore"])
            if visit["Ispettore"] in available_inspectors
            else 0,
            key=f"inspector_{visit_idx}",
        )

    with col3:
        st.markdown("#### 🎯 Stato")
        new_status = st.selectbox(
            "Stato:",
            options=["Da Confermare", "Confermato", "Annullato"],
            index=["Da Confermare", "Confermato", "Annullato"].index(
                visit.get("Stato", "Da Confermare")
            ),
            key=f"status_{visit_idx}",
        )

    # Notes
    st.markdown("#### 📝 Note")
    new_notes = st.text_area(
        "Note:",
        value=visit.get("Note", ""),
        key=f"notes_{visit_idx}",
        height=100,
    )

    # Save button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("💾 Salva Modifiche", use_container_width=True, type="primary"):
            # Update planning
            st.session_state.planning.at[visit_idx, "Ispettore"] = new_inspector
            st.session_state.planning.at[visit_idx, "Stato"] = new_status
            st.session_state.planning.at[visit_idx, "Note"] = new_notes

            st.success(f"{ICONS['success']} Modifiche salvate!")
            st.rerun()


# ============================================================================
# PAGE 4: HOLIDAYS & VACATIONS
# ============================================================================

def page_holidays():
    """Manage holidays and vacations."""
    st.title(f"{ICONS['vacation']} Ferie & Festività")

    tab1, tab2 = st.tabs(["📅 Festività Nazionali", "🏖️ Ferie Personale"])

    with tab1:
        render_holidays_tab()

    with tab2:
        render_vacations_tab()


def render_holidays_tab():
    """Render holidays management tab."""
    st.markdown("### 📅 Festività Nazionali")

    # Show custom holidays
    if len(st.session_state.custom_holidays) > 0:
        st.dataframe(st.session_state.custom_holidays)
    else:
        st.info("Nessuna festività personalizzata aggiunta")

    # Add new holiday
    st.markdown("### ➕ Aggiungi Festività")
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        new_holiday_date = st.date_input("Data", key="new_holiday_date")

    with col2:
        new_holiday_name = st.text_input("Nome", key="new_holiday_name")

    with col3:
        st.markdown("##")  # Spacing
        if st.button("Aggiungi", key="add_holiday"):
            if new_holiday_name:
                new_row = pd.DataFrame(
                    {"Data": [new_holiday_date], "Nome": [new_holiday_name]}
                )
                st.session_state.custom_holidays = pd.concat(
                    [st.session_state.custom_holidays, new_row], ignore_index=True
                )
                st.success(f"{ICONS['success']} Festività aggiunta")
                st.rerun()


def render_vacations_tab():
    """Render vacations management tab."""
    st.markdown("### 🏖️ Ferie & Assenze Personale")

    # Show existing vacations
    if len(st.session_state.vacations) > 0:
        st.dataframe(st.session_state.vacations)
    else:
        st.info("Nessuna assenza registrata")

    # Add new vacation
    st.markdown("### ➕ Aggiungi Assenza")

    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])

    with col1:
        vacation_inspector = st.selectbox(
            "Ispettore", options=ALL_INSPECTORS, key="vacation_inspector"
        )

    with col2:
        vacation_start = st.date_input("Dal", key="vacation_start")

    with col3:
        vacation_end = st.date_input("Al", key="vacation_end")

    with col4:
        vacation_type = st.selectbox(
            "Tipo", options=["Ferie", "Malattia", "Permesso"], key="vacation_type"
        )

    with col5:
        st.markdown("##")  # Spacing
        if st.button("Salva", key="add_vacation"):
            new_vacation = pd.DataFrame(
                {
                    "Ispettore": [vacation_inspector],
                    "Data_Inizio": [vacation_start],
                    "Data_Fine": [vacation_end],
                    "Tipo": [vacation_type],
                    "Note": [""],
                }
            )
            st.session_state.vacations = pd.concat(
                [st.session_state.vacations, new_vacation], ignore_index=True
            )
            st.success(f"{ICONS['success']} Assenza registrata")
            st.rerun()


# ============================================================================
# PAGE 5: EMAIL GENERATOR
# ============================================================================

def page_email():
    """Generate email templates for clients."""
    st.title(f"{ICONS['email']} Generatore Email Clienti")

    if st.session_state.planning is None or len(st.session_state.planning) == 0:
        st.warning(
            f"{ICONS['warning']} Nessun planning disponibile. Vai alla Home per generarlo."
        )
        return

    planning_df = st.session_state.planning

    st.markdown("### 1️⃣ Seleziona Visite")

    # Filter only "Da Confermare"
    pending_visits = planning_df[planning_df["Stato"] == "Da Confermare"]

    if len(pending_visits) == 0:
        st.info("Nessuna visita da confermare")
        return

    # Multi-select visits
    selected_indices = st.multiselect(
        "Seleziona visite:",
        options=pending_visits.index.tolist(),
        format_func=lambda i: f"{planning_df.loc[i, 'Data'].strftime('%d/%m')} - "
        f"{planning_df.loc[i, 'Nome del Cliente']} - "
        f"{planning_df.loc[i, 'Città']}",
    )

    if len(selected_indices) == 0:
        st.info("Seleziona almeno una visita")
        return

    st.success(f"{len(selected_indices)} visite selezionate")

    # Generate emails button
    if st.button("📨 Genera Email per Selezionati", type="primary"):
        selected_visits = planning_df.loc[selected_indices]
        emails = generate_bulk_emails(selected_visits)

        st.markdown("---")
        st.markdown("### 📧 Email Generate")

        for email_data in emails:
            with st.expander(f"▼ Email per {email_data['cliente']}"):
                st.code(email_data["email"], language="text")


# ============================================================================
# PAGE 6: STATISTICS
# ============================================================================

def page_stats():
    """Show statistics and KPIs."""
    st.title(f"{ICONS['stats']} Statistiche Planning")

    if st.session_state.planning is None or len(st.session_state.planning) == 0:
        st.warning(
            f"{ICONS['warning']} Nessun planning disponibile. Vai alla Home per generarlo."
        )
        return

    planning_df = st.session_state.planning

    # KPI Cards
    st.markdown("### 📊 KPI Generali")
    kpis = calculate_kpis(planning_df)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            f"{ICONS['visit']} Visite Totali",
            kpis["visite_totali"],
        )

    with col2:
        st.metric(
            f"{ICONS['confirmed']} Confermate",
            len(planning_df[planning_df["Stato"] == "Confermato"]),
        )

    with col3:
        st.metric(
            f"{ICONS['km']} Km Totali",
            f"{kpis['km_totali']:.0f}",
        )

    with col4:
        st.metric(
            f"{ICONS['time']} Ore Totali",
            f"{kpis['ore_totali']:.0f}",
        )

    st.markdown("---")

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Visite per Ispettore")
        inspector_stats = get_visits_by_inspector(planning_df)
        fig = px.bar(
            inspector_stats,
            x="Ispettore",
            y="Visite",
            color="Ispettore",
            color_discrete_map={
                inspector: get_inspector_color(inspector)
                for inspector in inspector_stats["Ispettore"]
            },
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Tour per Zona")
        zone_counts = planning_df["Tour_Zona"].value_counts()
        fig = px.pie(
            values=zone_counts.values,
            names=zone_counts.index,
            title="Distribuzione Tour",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Detailed table
    st.markdown("### 📋 Dettaglio per Ispettore")
    st.dataframe(get_visits_by_inspector(planning_df), use_container_width=True)

    # Export button
    st.markdown("---")
    if st.button("📥 Esporta Planning Excel", type="primary"):
        export_planning_excel()


def export_planning_excel():
    """Export planning to Excel file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"{PATHS['output_dir']}/Planning_Ispettori_{timestamp}.xlsx"

    # Ensure output directory exists
    os.makedirs(PATHS["output_dir"], exist_ok=True)

    format_planning_excel(
        st.session_state.planning,
        output_path,
        ALL_INSPECTORS,
    )

    st.success(f"{ICONS['success']} Planning esportato: {output_path}")

    # Also export renewals
    if st.session_state.renewals is not None:
        renewals_path = f"{PATHS['output_dir']}/Lista_Rinnovi_{timestamp}.xlsx"
        format_renewals_excel(st.session_state.renewals, renewals_path)
        st.success(f"{ICONS['success']} Lista rinnovi esportata: {renewals_path}")


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point."""
    # Render sidebar and get selected page
    page = render_sidebar()

    # Route to appropriate page
    if "Home" in page:
        page_home()
    elif "Gantt" in page:
        page_gantt()
    elif "Assegna" in page:
        page_assign()
    elif "Ferie" in page:
        page_holidays()
    elif "Email" in page:
        page_email()
    elif "Statistiche" in page:
        page_stats()


if __name__ == "__main__":
    main()
