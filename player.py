#!/usr/bin/env python
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep

DEVICE_ID="705764f3a36f0da9a46daac5325e50c79536c4c2"
CLIENT_ID="e3dda383fdb34d73b87bef1935814a66"
CLIENT_SECRET="67cba66d97fb4dddb1b0f8526cedb86e"

while True:
    try:
        reader=SimpleMFRC522()
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                       client_secret=CLIENT_SECRET,
                                                       redirect_uri="http://localhost:8888/callback",
                                                       scope="user-read-playback-state,user-modify-playback-state"))
        
        # create an infinite while loop that will always be waiting for a new scan
        while True:
            print("Waiting for record scan...")
            id= reader.read()[0]
            print("Card Value is:",id)
            sp.transfer_playback(device_id=DEVICE_ID, force_play=False)
            
            # DONT include the quotation marks around the card's ID value, just paste the number
            if (id==584194666005):
                #584194666005
                #
                print("play i wanna dance")
                # I wanna Dance
                sp.start_playback(device_id=DEVICE_ID, uris=['spotify:track:2tUBqZG2AbRi7Q0BIrVrEj'])
                sleep(2)
            if (id==584191323686):
                print("play don't stop believin")
                # playing a song
                sp.start_playback(device_id=DEVICE_ID, uris=['spotify:track:4bHsxqR3GMrXTxEPLuK5ue'])
                sleep(2)
            if (id==584194928153):
                print("play cyndi lauper album")
                # playing a song
                sp.start_playback(device_id=DEVICE_ID, context_uri='spotify:album:1FvdZ1oizXwF9bxogujoF0')
                sleep(2)
            if (id==584195452513):
                print("play kpoop playlist")
                # playing a song
                sp.start_playback(device_id=DEVICE_ID, context_uri='spotify:playlist:4Euq57Egm8s8GXQMfxANOw')
                sleep(2)                
            if (id==584197811781):
                print("play next track (from album)")
                # playing a song
                sp.next_track(device_id=DEVICE_ID)
                sleep(2)
            if (id==584195714661):
                print("play prev track (from album)")
                # playing a song
                sp.previous_track(device_id=DEVICE_ID)
                sleep(2)          
            elif (id==584195190301):
                print("play pause")
                # playing an album
                sp.pause_playback(device_id=DEVICE_ID)
                sleep(2)
                
            # continue adding as many "elifs" for songs/albums that you want to play

    # if there is an error, skip it and try the code again (i.e. timeout issues, no active device error, etc)
    except Exception as e:
        print(e)
        pass

    finally:
        print("Cleaning  up...")
        GPIO.cleanup()
