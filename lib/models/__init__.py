import sqlite3

CONN = sqlite3.connect('management.db')
CURSOR = CONN.cursor()
