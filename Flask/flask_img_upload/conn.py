import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE peoples (name TEXT, img_path TEXT)')
print("Table created successfully")
conn.close()
