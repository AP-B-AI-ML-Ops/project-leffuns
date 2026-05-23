FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# BRUTE FORCE INSTALL - needs to be ==0.4.28 to work or else it won't work
RUN pip install --no-cache-dir evidently==0.4.28 sqlalchemy psycopg2-binary

COPY . .

CMD ["python", "batch_score.py"]
