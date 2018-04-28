import sqlite3

connection = sqlite3.connect('API.db')
cursor = connection.cursor()

command = '''CREATE TABLE bots (
id INTEGER PRIMARY KEY,
guilds INTEGER,
members INTEGER,
token VARCHAR,
owner INTEGER
);'''

cursor.execute(command)
connection.commit()
connection.close()
