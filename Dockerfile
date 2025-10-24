FROM python:3.11-slim

WORKDIR /app
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

USER appuser
COPY src/ ./src/
RUN mkdir -p /app/data && chmod -R 777 /app/data

WORKDIR /app/src
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
