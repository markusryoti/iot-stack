FROM python:3.11-slim

WORKDIR /app

COPY collector.py .

RUN pip install --no-cache-dir requests

CMD ["python", "collector.py"]

