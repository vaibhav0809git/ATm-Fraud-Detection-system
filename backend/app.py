from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from fraud_detection import detect_fraud

app = Flask(__name__)
CORS(app)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('database/transactions.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create transactions table if it doesn't exist
def init_db():
    conn = get_db_connection()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        transaction_id TEXT NOT NULL UNIQUE,
        account_number TEXT NOT NULL,
        amount REAL NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    ''')
    conn.commit()
    conn.close()

@app.route('/api/transactions', methods=['POST'])
def add_transaction():
    data = request.json
    amount = data['amount']
    account_number = data['account_number']
    transaction_id = data['transaction_id']

    # Insert transaction into the database
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO transactions (transaction_id, account_number, amount) VALUES (?, ?, ?)',
                     (transaction_id, account_number, amount))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Transaction ID must be unique.'}), 400
    finally:
        conn.close()

import json

@app.route('/api/transactions', methods=['POST'])
def add_transaction():
    data = request.json
    amount = data['amount']
    account_number = data['account_number']
    transaction_id = data['transaction_id']

    # Insert transaction into the database
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO transactions (transaction_id, account_number, amount) VALUES (?, ?, ?)',
                     (transaction_id, account_number, amount))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Transaction ID must be unique.'}), 400
    finally:
        conn.close()

    # Check for fraud
    is_fraud = detect_fraud(amount)
    return jsonify({'is_fraud': is_fraud})
