#!/usr/bin/env python
import sqlite3

# connect to database
conn = sqlite3.connect('playlist.db')

# create a cursor
c = conn.cursor()

#create a table
c.execute("""CREATE TABLE playlist (
	rfid_tag text,
	uri text,
	uri_type text,
	uri_name text,
	uri_desc text,
	action text 
	)""")
# commit our table
conn.commit()
# close the conn
conn.close()
