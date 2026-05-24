FROM python:3.12-slim

WORKDIR /app

# Install curl so the container can ping the APIs
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY batch_score.py .

# Pause execution in a loop until Prefect is fully accepting connections
CMD while ! curl -s http://orchestration:4200/api/health > /dev/null; do echo "Waiting for Prefect..."; sleep 3; done; python batch_score.py
