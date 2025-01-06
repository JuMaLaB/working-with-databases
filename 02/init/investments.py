import sqlite3
import datetime

# Queries
create_table_query = """ 
CREATE TABLE investments (
    coin_id TEXT,
    currency TEXT,
    sell INT,
    amout REAL,
    date TIMESTAMP
)
"""
investements = ("bitcoin", "eur", True, 1.0, datetime.datetime.now())

# Code
database = sqlite3.connect("portfolio.db")
cursor = database.cursor()
cursor.execute(create_table_query)
cursor.execute("INSERT INTO investments VALUES (?, ?, ?, ?, ?);", investements)

"""
result = cursor.execute("SELECT * FROM investments")
first_or_none = result.fetchone()
print(first_or_none)
"""

# needed to save the data
database.commit()

# query data base
result = cursor.execute("SELECT * FROM investments")

all_rows = result.fetchall()
print(all_rows)

first_or_none = result.fetchone()
print(first_or_none)

""" (venv) λ py investments.py
('bitcoin', 'eur', 1, 1.0, '2025-01-06 15:46:32.592102')
[('bitcoin', 'eur', 1, 1.0, '2025-01-06 15:46:32.592102')]
None """