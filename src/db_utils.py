import sqlite3
from datetime import datetime

DB_PATH = "bias_ai.db"

def init_db():
    connect = sqlite3.connect(DB_PATH)
    c = connect.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            source TEXT,
            url TEXT,
            summary TEXT,
            leaning TEXT,
            topic TEXT,
            bias_explanation TEXT,
            date_fetched TEXT
        )
    ''')
    connect.commit()
    connect.close()

def save_article(title, source, url, summary, leaning, topic, explanation):
    date_fetched = datetime.now().isoformat() 
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO articles (title, source, url, summary, leaning, topic, bias_explanation, date_fetched)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (title, source, url, summary, leaning, topic, explanation, date_fetched))
    conn.commit()
    conn.close()

def fetch_all_articles():
    connect = sqlite3.connect(DB_PATH)
    c = connect.cursor()
    c.execute('SELECT * FROM articles ORDER BY date_fetched ASC')
    rows = c.fetchall()
    connect.close()
    return rows
