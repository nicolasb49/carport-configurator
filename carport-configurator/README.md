# Carport-Configurator Webanwendung

Dieses Projekt bietet eine einfache Basis, um eine Webanwendung zur Konfiguration von Carports zu entwickeln.

## Installation

1. Python 3 installieren.
2. Optional: Ein virtuelles Environment anlegen:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```

## Starten

Backend starten mit uvicorn:
```bash
uvicorn backend.main:app --reload
```

Frontend über Streamlit starten:
```bash
streamlit run frontend/main.py
```

