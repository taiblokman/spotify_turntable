import sqlite3

conn = sqlite3.connect('playlist.db')

c= conn.cursor()

c.execute("SELECT * from playlist")

items = c.fetchall()

for item in items:
	print(item)

conn.commit()
conn.close()
