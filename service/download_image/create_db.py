import sqlite3
import pandas as pd
conn = sqlite3.connect('./../../database/brightside.db')

conn.execute('''CREATE TABLE news (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   url text NOT NULL,
   des text NOT NULL
);''')

conn.execute('''CREATE TABLE images (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   url text NOT NULL,
   des text NOT NULL
);''')
conn.close()
