from flask import Flask, jsonify, request
import psycopg2
import os
import logging
import random
import time

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def get_db():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        database=os.environ.get('DB_NAME', 'payments'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASS', 'postgres')
    )

@app.route('/health')
def health():
    logging.info("Health check called")
    return jsonify({"status": "ok"})

@app.route('/payment', methods=['POST'])
def process_payment():
    data = request.json
    amount = data.get('amount', 0)
    ref = f"PAY-{random.randint(1000,9999)}"
    logging.info(f"Processing payment {ref} for amount {amount}")
    time.sleep(0.1)
    return jsonify({"reference": ref, "status": "success", "amount": amount})

@app.route('/transactions')
def transactions():
    logging.info("Fetching transactions")
    return jsonify({"transactions": [], "count": 0})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
