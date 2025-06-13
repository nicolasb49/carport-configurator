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
uvicorn backend.app:app --reload
```

Frontend über Streamlit starten:
```bash
streamlit run frontend/app.py
```

## Docker

Die Anwendung kann auch komplett in einem Container gebaut und gestartet werden.

Zum Erstellen des Images im Projektverzeichnis ausführen:

```bash
docker build -t carport-configurator .
```

Anschließend lässt sich der Container starten:

```bash
docker run -p 8000:8000 -p 8501:8501 carport-configurator
```

Das Backend ist dann unter `http://localhost:8000` erreichbar und das
Frontend unter `http://localhost:8501`.

