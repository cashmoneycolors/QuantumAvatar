FROM python:3.9-slim

# Arbeitsverzeichnis setzen
WORKDIR /app

# Systemabhängigkeiten installieren
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python Dependencies kopieren und installieren
COPY ../requirements.txt .
COPY ../requirements-fixed.txt .
RUN pip install --no-cache-dir -r requirements-fixed.txt

# Anwendungscode kopieren
COPY ../ .

# Port setzen
EXPOSE 5000

# Production Server starten
CMD ["python", "production_http_server.py"]
