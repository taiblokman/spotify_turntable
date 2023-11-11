#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()
#reader.authenticate(0xFFFFFFFFFFFFFFFF)

try:
    while True:
        print("Waiting for you to scan an RFID sticker/card")
        id = reader.read()[0]
        #if id is not None and id.startswith('NTAG213'):
            #print('NTAG213')
        print("The ID for this card is:", id)
        
finally:
        GPIO.cleanup()