import unicodedata
import requests
import sqlite3
import time

#Configuration 
tokens = ['app-tO1fBXNSg5kiT6abrgoAx6FC']
endpoint = 'http://10.30.10.104/v1'
db_path = f'dify_logs_{int(time.time())}.db'

# Initialize SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS conversations (id INTEGER PRIMARY KEY AUTOINCREMENT)