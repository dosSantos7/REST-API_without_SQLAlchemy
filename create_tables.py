import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

query = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
# for auto-incrementing values, we need to write the full 'INTEGER' instead of 'int'
cursor.execute(query)

query = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(query)

connection.commit()
connection.close()
