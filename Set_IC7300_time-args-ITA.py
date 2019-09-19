#! /d/Python/Python37/python
#
# IC-7300 time sync by Kevin Loughin, KB9RLW. June 2019
# Ver. 1.0
# This script will set the Icom 7300 internal clock based on your computer
# clock.  Provided your computer clock is synced to network time, this
# should insure your radio's clock is within a fraction of a second of
# standard time.
#
# Below are three variables you need to change to match your location and
# radio.  If your computer clock is not set to Universal time, set the 
# offset value.
# Also the serial port name for your IC-7300 on your computer. Change to 
# match your setup. i.e. COM3 or similar for windows.
#
#Aggiunta import della libreria sys per la gestione degli argomenti su command line
import sys

baudrate = int(sys.argv[1])  #change to match your radio
gmtoffset = 0  #change to a negative or positive offset from GMT if you
#               want to use local time.  i.e. -5 for EST
serialport = str(sys.argv[2])  # Serial port of your radios serial interface.
baudratestr = str(baudrate)

# Defining the command to set the radios time in hex bytes.
preamble = ["0xFE", "0xFE", "0x94", "0xE0", "0x1A", "0x05", "0x00", "0x95"]
postamble = "0xfd"

# Windows chatting
#
print ("")
print ("Sto veramente funzionando su MS Winzozz, grazie a IW2NOY ! :-)")
print ("Servo per sincronizzare l'orario GMT del PC su IC-7300...")
print ("Mi connetterò sulla porta " + serialport + " alla velocità di " + baudratestr)
print("")
print("Attenderò che l'orario raggiunga i secondi 00, prima di inviare i dati al IC-7300")
print("")
#Import libraries we'll need to use
import time
import serial
import struct

# Here we get the computers current time in hours and minutes.
# Add in the offset, if any, and roll over if we exceed 23 or go below 0
# hours.  Finally appending hex byte formated time data to the command string.
t = time.localtime()
hours = time.strftime("%H")
hours = int(hours) + gmtoffset
if hours < 0:
    hours = 23 + hours
if hours > 23:
    hours = 23 - hours
hours = str(hours)

if (len(hours) < 2):
    hours = "0" + str(hours)
hours = "0x" + hours
preamble.append(hours)

minutes = (int(time.strftime("%M")) + 1)
minutes = str(minutes)
if (len(minutes) < 2):
    minutes = "0" + minutes
minutes = "0x" + minutes
preamble.append(minutes)
preamble.append('0xFD')

# Now I get the current computer time in seconds.  Needed to set the time only
# at the top of the minute.
seconds = int(time.strftime("%S"))

# Now we wait for the top of the minute.
lastsec = 1
while(seconds != 0):
   t = time.localtime()
   seconds = int(time.strftime("%S"))
   if(seconds != lastsec):
        lastsec = seconds
   time.sleep(.01)

# Now that we've reached the top of the minute, set the radios time!
ser = serial.Serial(serialport, baudrate)

count = 0
while(count < 11):
    senddata = int(bytes(preamble[count], 'UTF-8'), 16)
    # Aggiunta di IW2NOY per debugging dei dati inviati
    #dati = str(senddata)
    #giro = str(count)
    #print ("Dati inviati a IC-7300 al giro " + giro  + " : " + dati)
    # Fine aggiunta
    ser.write(struct.pack('>B', senddata))
    count = count +1

ser.close()

print ("Dati inviati correttamente a IC-7300! L'orario dovrebbe essere stato sincronizzato!")
# All done.  The radio is now in sync with the computer clock.
