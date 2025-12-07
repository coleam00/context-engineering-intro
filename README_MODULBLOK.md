# 🚗 Modulblok Inspection Planning System

Sistema web interattivo per la pianificazione e gestione ottimizzata delle visite ispettive presso Modulblok SPA.

---

## 📋 Indice

- [Panoramica](#panoramica)
- [Funzionalità](#funzionalità)
- [Requisiti](#requisiti)
- [Installazione](#installazione)
- [Utilizzo](#utilizzo)
- [Struttura File Excel](#struttura-file-excel)
- [Architettura](#architettura)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Panoramica

Il sistema Modulblok Planning ottimizza automaticamente le visite ispettive per 4 ispettori su tutto il territorio nazionale italiano, minimizzando km e tempo di viaggio attraverso:

- **Matching automatico** ordini ↔ anagrafica clienti
- **Geocoding** indirizzi con OpenStreetMap
- **Clustering geografico** con K-means
- **Ottimizzazione TSP** (Travelling Salesman Problem) con algoritmo Nearest Neighbor
- **Pianificazione giornaliera** rispettando vincoli di lavoro
- **Vista Gantt interattiva** per gestione calendario settimanale

### 👥 Ispettori

- **Adrian** (base Pagnacco, UD) - Copertura nazionale
- **Salvatore** (base Pagnacco, UD) - Copertura nazionale
- **Mattia** (base Pagnacco, UD) - Copertura nazionale
- **Paolo** (base Milano) - **SOLO** Lombardia, Piemonte, Liguria, Valle d'Aosta

---

## ✨ Funzionalità

### 📱 Pagine Applicazione

1. **🏠 Home** - Carica file Excel e genera planning ottimizzato
2. **📅 Gantt Calendario** - Vista calendario settimanale con filtri
3. **✏️ Assegna Ispettori** - Modifica assegnazioni manualmente
4. **🏖️ Ferie & Festività** - Gestione ferie e giorni festivi
5. **📧 Email Clienti** - Genera proposte email per conferme
6. **📊 Statistiche** - KPI e statistiche dettagliate

### 🔑 Funzionalità Chiave

- ✅ Ottimizzazione automatica percorsi con TSP
- ✅ Vincolo Paolo (solo 4 regioni del Nord-Ovest)
- ✅ Gestione ferie e festività
- ✅ Vista Gantt interattiva
- ✅ Export Excel completo
- ✅ Generazione email automatica
- ✅ KPI e statistiche real-time

---

## 🔧 Requisiti

### Software

- Python 3.8 o superiore
- pip (gestore pacchetti Python)
- Excel o LibreOffice per visualizzare output

### Dipendenze Python

Tutte le dipendenze sono elencate in `requirements.txt`:

```
pandas>=2.0.0
openpyxl>=3.1.0
geopy>=2.4.0
scikit-learn>=1.3.0
streamlit>=1.30.0
plotly>=5.18.0
```

---

## 🚀 Installazione

### 1. Clone del Repository

```bash
git clone <repository-url>
cd context-engineering-intro
```

### 2. Creazione Virtual Environment

**Linux/macOS:**
```bash
python3 -m venv venv_linux
source venv_linux/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Installazione Dipendenze

```bash
pip install -r requirements.txt
```

### 4. Creazione File Template

```bash
python create_templates.py
```

Questo crea file Excel di esempio in `data/templates/`:
- `Anagrafica_Template.xlsx` - Template anagrafica clienti
- `Ordini_Template.xlsx` - Template ordini confermati
- `Anagrafica_Test.xlsx` - Dati test (20 clienti)
- `Ordini_Test.xlsx` - Dati test (12 ordini)

---

## 📖 Utilizzo

### Avvio Applicazione

```bash
streamlit run app.py
```

L'applicazione si aprirà automaticamente nel browser su `http://localhost:8501`

### Workflow Completo

1. **📤 Upload File Excel** (Pagina Home)
   - Carica `Anagrafica_Clienti.xlsx`
   - Carica `Ordini_Confermati.xlsx`
   - Click su "🚀 GENERA PLANNING"

2. **⏳ Attendi Generazione** (2-3 minuti per geocoding)
   - Progress bar mostra avanzamento
   - Al termine: planning completo disponibile

3. **📅 Visualizza Gantt** (Pagina Gantt Calendario)
   - Vista calendario settimanale
   - Filtra per ispettore/regione/stato
   - Verifica distribuzione visite

4. **✏️ Modifica Assegnazioni** (Pagina Assegna Ispettori)
   - Seleziona visita
   - Cambia ispettore (rispettando vincolo Paolo)
   - Modifica stato/note

5. **🏖️ Gestisci Ferie** (Pagina Ferie & Festività)
   - Aggiungi periodi ferie
   - Aggiungi festività personalizzate

6. **📧 Genera Email** (Pagina Email Clienti)
   - Seleziona visite da confermare
   - Genera email template
   - Copia e invia

7. **📥 Export Finale** (Pagina Statistiche)
   - Click "📥 Esporta Planning Excel"
   - File salvato in `data/output/`

---

## 📊 Struttura File Excel

### Anagrafica_Clienti.xlsx

**Colonne richieste:**

| Colonna | Tipo | Esempio | Descrizione |
|---------|------|---------|-------------|
| ID Cliente | Numero | 18923 | ID univoco cliente |
| Nome del Cliente | Testo | "3A MCOM SRL" | Ragione sociale |
| Indirizzo completo | Testo | "ZONA INDUSTRIALE, 4" | Indirizzo sede |
| CAP | Testo | "38055" | Codice postale |
| Città | Testo | "GRIGNO" | Città |
| Regione | Testo | "Trentino-Alto Adige" | Regione |
| Ore lavoro | Numero | 2.5 | Ore stimate visita |
| Data visita di riferimento 2026 | Data | "04/11/2026" | Scadenza contratto |

### Ordini_Confermati.xlsx

**Colonne richieste:**

| Colonna | Tipo | Esempio | Descrizione |
|---------|------|---------|-------------|
| ID_Ordine | Testo | "W2500547-000" | Numero ordine |
| Cliente | Testo | "FORMA CUCINE SPA" | Nome cliente (deve matchare anagrafica) |
| Indirizzo_Sede | Testo | "VIA G.DI VITTORIO, 25" | Indirizzo (deve matchare anagrafica) |
| Data_Ordine | Data | "25/08/2025" | Data ordine (opzionale) |

**⚠️ IMPORTANTE:**
- **Cliente** e **Indirizzo_Sede** devono corrispondere ESATTAMENTE a quelli in Anagrafica
- Spazi extra e maiuscole/minuscole vengono normalizzati automaticamente
- Solo ordini matchati vengono pianificati

---

## 🏗️ Architettura

### Struttura Progetto

```
context-engineering-intro/
├── app.py                    # Streamlit web application
├── config.py                 # Configurazioni e costanti
├── utils.py                  # Funzioni utility
├── planner_engine.py         # Core optimization logic
├── create_templates.py       # Script creazione template
├── requirements.txt          # Dipendenze Python
├── PLANNING.md              # Documentazione architettura
├── TASK.md                  # Task tracker
├── data/
│   ├── templates/           # Template Excel
│   └── output/              # Export finali
└── tests/
    ├── test_utils.py
    ├── test_planner_engine.py
    └── conftest.py
```

### Algoritmi Principali

**1. Matching Ordini ↔ Anagrafica**
```python
# Normalizzazione stringhe
CLIENTE_NORM = uppercase + trim + collapse whitespace
# Inner join su (Cliente, Indirizzo)
```

**2. Geocoding**
```python
# Nominatim (OpenStreetMap)
Query: "{CAP} {Città}, Italia"
Fallback: coordinate regionali
Rate limit: 1 req/sec
```

**3. K-means Clustering**
```python
# Clustering geografico su (lat, lon)
n_clusters = 8 (configurabile)
```

**4. TSP Nearest Neighbor**
```python
1. Start = cliente più vicino a base
2. Loop: next = più vicino al precedente
3. Return = tour ottimizzato
```

**5. Scheduling Giornaliero**
```python
Vincoli:
- Max 8h/giorno (viaggio + lavoro)
- No weekend
- No festività
- Venerdì: max 6.5h (rientro 17:30)
```

---

## 🧪 Testing

### Esecuzione Test

```bash
# Attiva virtual environment
source venv_linux/bin/activate

# Tutti i test
pytest

# Con coverage
pytest --cov=. --cov-report=html

# Verbose
pytest -v

# Test specifico
pytest tests/test_utils.py::test_normalize_string_basic
```

### Test Coperti

- ✅ Normalizzazione stringhe
- ✅ Matching ordini (exact, case-insensitive, whitespace)
- ✅ Calcolo distanze
- ✅ Vincolo Paolo
- ✅ TSP ottimizzazione
- ✅ Scheduling giornaliero (8h limit, weekend skip)
- ✅ Gestione ferie/festività
- ✅ Validazione file Excel

---

## 🐛 Troubleshooting

### Problema: "Nessun ordine matchato"

**Causa:** Nomi/indirizzi non corrispondono tra anagrafica e ordini

**Soluzione:**
1. Verifica che Cliente e Indirizzo siano identici
2. Sistema mostra gli ordini non matchati
3. Correggi i dati e ricarica

**Esempio:**
```
Anagrafica: "FORMA CUCINE SPA" | "VIA G.DI VITTORIO, 25"
Ordini:     "FORMA CUCINE SPA" | "VIA G.DI  VITTORIO, 25"  ❌ (doppio spazio)
```

### Problema: Geocoding lento

**Causa:** Nominatim rate limit (1 richiesta/secondo)

**Comportamento atteso:**
- 50 indirizzi = ~1 minuto
- 100 indirizzi = ~2 minuti
- Progress bar mostra avanzamento

**Nota:** Questo è normale e non può essere accelerato (limite API gratuita)

### Problema: "Paolo non può andare in [regione]"

**Causa:** Tentativo assegnazione Paolo fuori dalle sue regioni

**Soluzione:**
- Paolo può lavorare SOLO in: Lombardia, Piemonte, Liguria, Valle d'Aosta
- Per altre regioni scegli: Adrian, Salvatore, Mattia

### Problema: File Excel non si apre in export

**Causa:** File potrebbe essere aperto in altro programma

**Soluzione:**
1. Chiudi Excel/LibreOffice
2. Il sistema genera file con timestamp unico
3. Controlla `data/output/` per file più recente

### Problema: Date saltano weekend

**Causa:** Questo è il comportamento corretto!

**Spiegazione:**
- Sistema salta automaticamente sabato/domenica
- Se visita cade in weekend → sposta a lunedì

---

## 📞 Supporto

**Progetto:** Modulblok Planning System
**Cliente:** Modulblok SPA - Area SERVICE
**Sito:** www.modulblok.com

### Segnalazione Bug

Per segnalare bug o richiedere funzionalità:
1. Descrivi il problema
2. Allega screenshot se possibile
3. Specifica dati di input (senza informazioni sensibili)

---

## 🎯 Vincoli Importanti

### 1. Vincolo Paolo ⚠️

**CRITICO:** Paolo può lavorare SOLO in:
- Lombardia
- Piemonte
- Liguria
- Valle d'Aosta

Tutte le altre regioni → Adrian, Salvatore, Mattia

### 2. Vincoli Lavorativi

- **8 ore/giorno** massimo (incluso viaggio)
- **No sabato/domenica**
- **No festività nazionali**
- **Venerdì: 6.5h max** (rientro entro 17:30)
- **Buffer: +0.5h** per imprevisti

### 3. Matching Ordini

- Solo ordini con match in anagrafica vengono pianificati
- Match su: (Cliente + Indirizzo) normalizzati
- Case-insensitive e trim whitespace automatico

---

## 📈 Metriche di Successo

Il sistema considera il planning ottimale quando:

✅ Tutti gli ordini confermati sono matchati
✅ Visite raggruppate geograficamente
✅ Km totali minimizzati
✅ Vincolo Paolo rispettato al 100%
✅ Nessuna visita in weekend/festività
✅ Ogni giorno < 8h (incluso viaggio)

---

## 🔮 Roadmap Future (Non implementato)

Phase 2 potrebbe includere:
- Google Maps API per distanze reali
- Integrazione SMTP per invio email
- Export PDF con branding Modulblok
- Multi-utente con autenticazione
- Database PostgreSQL
- Mobile responsive design
- Machine Learning per predizioni tempi

---

## 📝 Changelog

### v1.0.0 (2025-12-07)
- ✅ Sistema completo implementato
- ✅ Tutte le 6 pagine funzionanti
- ✅ TSP optimization
- ✅ Vincolo Paolo
- ✅ Export Excel
- ✅ Test coverage > 80%

---

## 📄 Licenza

Proprietario: Modulblok SPA
Tutti i diritti riservati © 2025

---

**🚀 Buon lavoro con Modulblok Planning System!**
