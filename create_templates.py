"""
Script to create template Excel files for Modulblok Planning System.

Run this script to generate sample Excel files with the correct structure.
"""

import pandas as pd
from datetime import datetime, timedelta


def create_anagrafica_template():
    """Create Anagrafica_Clienti template Excel file."""
    # Sample data
    data = {
        "ID Cliente": [18923, 19001, 19002, 19003, 19004],
        "Nome del Cliente": [
            "3A MCOM SRL",
            "FORMA CUCINE SPA",
            "INDUSTRIE MECCANICHE SRL",
            "TESSUTI EUROPA SPA",
            "LOGISTICA MODERNA SRL",
        ],
        "Indirizzo completo": [
            "ZONA INDUSTRIALE, 4",
            "VIA G.DI VITTORIO, 25",
            "VIA DELLA REPUBBLICA, 10",
            "CORSO ITALIA, 45",
            "VIA DELL'INDUSTRIA, 8",
        ],
        "CAP": ["38055", "30029", "33100", "20100", "10100"],
        "Città": ["GRIGNO", "SANTO STINO DI LIVENZA", "UDINE", "MILANO", "TORINO"],
        "Regione": [
            "Trentino-Alto Adige",
            "Veneto",
            "Friuli-Venezia Giulia",
            "Lombardia",
            "Piemonte",
        ],
        "Ore lavoro": [2.5, 3.0, 4.0, 2.5, 3.5],
        "Data visita di riferimento 2026": [
            "04/11/2026",
            "15/03/2026",
            "20/04/2026",
            "10/05/2026",
            "25/06/2026",
        ],
    }

    df = pd.DataFrame(data)
    df.to_excel("data/templates/Anagrafica_Template.xlsx", index=False)
    print("✅ Created: data/templates/Anagrafica_Template.xlsx")
    print(f"   Rows: {len(df)}")


def create_ordini_template():
    """Create Ordini_Confermati template Excel file."""
    data = {
        "ID_Ordine": ["W2500547-000", "W2500548-000", "W2500549-000"],
        "Cliente": ["FORMA CUCINE SPA", "INDUSTRIE MECCANICHE SRL", "LOGISTICA MODERNA SRL"],
        "Indirizzo_Sede": [
            "VIA G.DI VITTORIO, 25",
            "VIA DELLA REPUBBLICA, 10",
            "VIA DELL'INDUSTRIA, 8",
        ],
        "Data_Ordine": ["25/08/2025", "10/09/2025", "15/09/2025"],
    }

    df = pd.DataFrame(data)
    df.to_excel("data/templates/Ordini_Template.xlsx", index=False)
    print("✅ Created: data/templates/Ordini_Template.xlsx")
    print(f"   Rows: {len(df)}")


def create_test_data():
    """Create larger test data files for realistic testing."""
    # More realistic anagrafica with 20 clients
    today = datetime.now()

    clients = []
    for i in range(1, 21):
        # Vary expiration dates
        days_offset = 30 + (i * 10)  # Range from 30 to 230 days
        expiry_date = (today + timedelta(days=days_offset)).strftime("%d/%m/%Y")

        # Distribute across regions
        regions = [
            ("Friuli-Venezia Giulia", "UDINE", "33100"),
            ("Veneto", "VENEZIA", "30100"),
            ("Lombardia", "MILANO", "20100"),
            ("Piemonte", "TORINO", "10100"),
            ("Liguria", "GENOVA", "16100"),
            ("Toscana", "FIRENZE", "50100"),
            ("Emilia-Romagna", "BOLOGNA", "40100"),
            ("Lazio", "ROMA", "00100"),
        ]

        region_info = regions[i % len(regions)]

        client = {
            "ID Cliente": 19000 + i,
            "Nome del Cliente": f"CLIENTE TEST {i} SRL",
            "Indirizzo completo": f"VIA TEST {i}",
            "CAP": region_info[2],
            "Città": region_info[1],
            "Regione": region_info[0],
            "Ore lavoro": 2.0 + (i % 5) * 0.5,
            "Data visita di riferimento 2026": expiry_date,
        }
        clients.append(client)

    anagrafica_df = pd.DataFrame(clients)
    anagrafica_df.to_excel("data/templates/Anagrafica_Test.xlsx", index=False)
    print("✅ Created: data/templates/Anagrafica_Test.xlsx")
    print(f"   Rows: {len(anagrafica_df)}")

    # Create orders for first 12 clients (to test matching)
    orders = []
    for i in range(1, 13):
        client = clients[i - 1]
        order = {
            "ID_Ordine": f"ORD-2025-{i:04d}",
            "Cliente": client["Nome del Cliente"],
            "Indirizzo_Sede": client["Indirizzo completo"],
            "Data_Ordine": (today - timedelta(days=30 - i)).strftime("%d/%m/%Y"),
        }
        orders.append(order)

    ordini_df = pd.DataFrame(orders)
    ordini_df.to_excel("data/templates/Ordini_Test.xlsx", index=False)
    print("✅ Created: data/templates/Ordini_Test.xlsx")
    print(f"   Rows: {len(ordini_df)}")


if __name__ == "__main__":
    import os

    # Create templates directory if not exists
    os.makedirs("data/templates", exist_ok=True)

    print("\n🚀 Generazione template Excel...\n")

    create_anagrafica_template()
    create_ordini_template()
    create_test_data()

    print("\n✅ Tutti i template sono stati creati!")
    print("\n📁 File disponibili:")
    print("   - data/templates/Anagrafica_Template.xlsx (esempio base)")
    print("   - data/templates/Ordini_Template.xlsx (esempio base)")
    print("   - data/templates/Anagrafica_Test.xlsx (test con 20 clienti)")
    print("   - data/templates/Ordini_Test.xlsx (test con 12 ordini)")
