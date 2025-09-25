import sqlite3
import threading
from contextlib import closing
from pathlib import Path
import os

DB_FILENAME = 'pos_data.db'
DB_LOCK = threading.Lock()

def get_db_path():
    return Path(os.getcwd()) / DB_FILENAME

def init_db():
    db_path = get_db_path()
    with DB_LOCK, closing(sqlite3.connect(str(db_path))) as conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT,
            role TEXT,
            created_at TEXT
        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            note TEXT
        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT UNIQUE,
            name TEXT,
            category_id INTEGER,
            price REAL,
            stock INTEGER,
            tax_percent REAL DEFAULT 0,
            discount_percent REAL DEFAULT 0,
            barcode TEXT
        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE,
            total REAL,
            discount REAL,
            tax REAL,
            user_id INTEGER,
            created_at TEXT
        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS transaction_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id INTEGER,
            product_id INTEGER,
            qty INTEGER,
            price REAL,
            discount REAL,
            tax REAL
        )''')
        conn.commit()

def execute(query, params=(), fetch=False):
    db_path = get_db_path()
    with DB_LOCK, closing(sqlite3.connect(str(db_path))) as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        if fetch:
            return cur.fetchall()
        conn.commit()
        return None
