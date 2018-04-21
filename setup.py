import sqlite3

connection = sqlite3.connect('API.db')
cursor = connection.cursor()

command = '''CREATE TABLE bots (
id INTEGER,
guilds INTEGER,
members INTEGER
);'''

cursor.execute(command)
connection.commit()
connection.close()
