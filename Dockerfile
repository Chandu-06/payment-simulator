FRM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

RUN pip install flask psycopg2-binary --no-cache-dir

COPY app.py .

EXPOSE 8000

CMD ["python", "app.py"]
