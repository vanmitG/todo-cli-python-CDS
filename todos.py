import os
import sys
import fire
import code
import sqlite3
from datetime import datetime
from termcolor import colored
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')
conn = sqlite3.connect(DEFAULT_PATH)

sql = """
  CREATE TABLE IF NOT EXISTS todos(
    id INTEGER PRIMARY KEY,
    body TEXT NOT NULL,
    due_date TEXT NOT NULL,
    status TEXT DEFAULT "incomplete"
  )
"""

cur = conn.cursor()
cur.execute(sql)
# print("sql", sql)
if __name__ == '__main__':
    try:
        print('Yes!!!Main function executing', sys.argv[1])

    except IndexError:
        print("IndexError")
