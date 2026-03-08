import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'agribag.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS farmers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_name TEXT NOT NULL,
            date TEXT NOT NULL,
            total_weight REAL NOT NULL,
            col1_sum REAL,
            col2_sum REAL,
            col3_sum REAL,
            col4_sum REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def save_record(farmer_name, date, total_weight, column_sums):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO farmers (farmer_name, date, total_weight, col1_sum, col2_sum, col3_sum, col4_sum)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        farmer_name,
        date,
        total_weight,
        column_sums[0],
        column_sums[1],
        column_sums[2],
        column_sums[3]
    ))
    
    conn.commit()
    conn.close()

def delete_record(record_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM farmers WHERE id = ?', (record_id,))
    
    conn.commit()
    conn.close()

def get_all_records():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM farmers ORDER BY created_at DESC')
    records = cursor.fetchall()
    
    conn.close()
    return records

def get_farmer_records(farmer_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM farmers WHERE farmer_name = ? ORDER BY created_at DESC', (farmer_name,))
    records = cursor.fetchall()
    
    conn.close()
    return records