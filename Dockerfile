FROM python:3.11-slim

WORKDIR /app

RUN pip install flask psycopg2-binary --no-cache-dir

COPY app.py .

EXPOSE 8000

CMD ["python", "app.py"]
