#!/usr/bin/env python
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import spotipy
import sqlite3
from spotipy.oauth2 import SpotifyOAuth
from time import sleep

DEVICE_ID="705764f3a36f0da9a46daac5325e50c79536c4c2"
CLIENT_ID="e3dda383fdb34d73b87bef1935814a66"
CLIENT_SECRET="67cba66d97fb4dddb1b0f8526cedb86e"
PLAYLIST_DB="playlist.db"

# Connect to the SQLite database
connection = sqlite3.connect(PLAYLIST_DB)
cursor = connection.cursor()
# Execute a query to retrieve data
cursor.execute('SELECT rfid_tag, uri, uri_type, uri_name, uri_desc, action FROM mimispotify')
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
print(my_dict)



while True:
    try:
        reader=SimpleMFRC522()
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                       client_secret=CLIENT_SECRET,
                                                       redirect_uri="http://localhost:8888/callback",
                                                       scope="user-read-playback-state,user-modify-playback-state"))
        
        sp.volume(100, device_id=DEVICE_ID)
        # create an infinite while loop that will always be waiting for a new scan
        while True:
            print("Waiting for record scan...")
            id= reader.read()[0]
            print("Card Value is:",id)
            print("URI is",my_dict[id]['uri_name'])
            sp.transfer_playback(device_id=DEVICE_ID, force_play=False)
            
            if (my_dict[id]['uri_type'] == "action"):
                print("take an action")
                if (my_dict[id]['action'] == "next"):
                    sp.next_track(device_id=DEVICE_ID)
                    sleep(2)
                if (my_dict[id]['action'] == "previous"):
                    sp.previous_track(device_id=DEVICE_ID)
                    sleep(2)
                if (my_dict[id]['action'] == "pause"):
                    sp.pause_playback(device_id=DEVICE_ID)
                    sleep(2)                    
            elif (my_dict[id]['uri_type'] != "action"):
            # play a song
                if (my_dict[id]['uri_type'] == "playlist"):
                    CONTEXT_URI = "spotify:playlist:" + my_dict[id]['uri']
                    sp.start_playback(device_id=DEVICE_ID, context_uri=CONTEXT_URI)
                    sleep(2)
                if (my_dict[id]['uri_type'] == "album"):
                    CONTEXT_URI = "spotify:album:" + my_dict[id]['uri']
                    sp.start_playback(device_id=DEVICE_ID, context_uri=CONTEXT_URI)
                    sleep(2)
                if (my_dict[id]['uri_type'] == "track"):
                    CONTEXT_URI = "spotify:track:" + my_dict[id]['uri']
                    sp.start_playback(device_id=DEVICE_ID, uris=[CONTEXT_URI])
                    sleep(2)                    
            # DONT include the quotation marks around the card's ID value, just paste the number

                
            # continue adding as many "elifs" for songs/albums that you want to play

    # if there is an error, skip it and try the code again (i.e. timeout issues, no active device error, etc)
    except Exception as e:
        print(e)
        pass

    finally:
        print("Cleaning  up...")
        GPIO.cleanup()
