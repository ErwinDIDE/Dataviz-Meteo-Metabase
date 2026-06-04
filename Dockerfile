# Image Python
FROM python:3.11-slim

# Dossier conteneur
WORKDIR /app

# Dépendances PostgreSQL
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Installation des dépendances
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du projet
COPY . .

# Execution script
CMD ["python", "src/main.py"]
