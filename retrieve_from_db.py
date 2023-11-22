
import sqlite3

# Connect to the SQLite database
connection = sqlite3.connect('playlist.db')
cursor = connection.cursor()

# Execute a query to retrieve data
cursor.execute('SELECT rfid_tag, uri, uri_type, uri_name, uri_desc, action FROM playlist')

# Initialize an empty dictionary
my_dict = {}

# Fetch data and populate the dictionary
for row in cursor.fetchall():
    rfid_tag, uri, uri_type, uri_name, uri_desc, action = row
    # Using rfid as the key in the dictionary
    my_dict[rfid_tag] = {
        'uri': uri,
        'uri_type': uri_type,
        'uri_name': uri_name,
        'desc': uri_desc,
        'action': action
    }

# Close the database connection
connection.close()

# Now, my_dict contains the data from the SQLite database
print(my_dict)
print(my_dict['584195452513']['desc'])

# Assuming you have already populated your dictionary (my_dict) from the SQLite database

# Specify the nested key you're interested in (e.g., 'uri_name')
specific_nested_key = 'uri_name'

# Retrieve all values for the specified nested key
values_for_specific_key = [entry[specific_nested_key] for entry in my_dict.values()]

# Print the results
print(f"All values for the nested key '{specific_nested_key}':")
print(values_for_specific_key)


