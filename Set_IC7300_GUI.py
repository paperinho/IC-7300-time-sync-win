#! /d/Python/Python37/python

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel, QComboBox, QMessageBox, QProgressBar
from PyQt5 import QtGui 

# Application and windows design
app = QApplication([])
window = QWidget()
layout = QGridLayout()
labelsel = QLabel('Selezionare la porta seriale:')
combosel = QComboBox()
labelbaud = QLabel('Selezionare la velocità della porta seriale:')
combobaud = QComboBox()
combobaud.addItems(['4800', '9600', '19200', '38400', '57600', '115200'])
labelapp = QLabel('IC-7300 Time & Date Sync by IW2NOY')
buttonsync = QPushButton('Sync IC-7300!')
buttonquit = QPushButton('Chiudi')
progressbar = QProgressBar()

# First row
layout.addWidget(labelapp, 0,0,1,2)
labelapp.setFont(QtGui.QFont("Verdana", 12, QtGui.QFont.Bold)) # This use QtGui
# Second row
layout.addWidget(labelsel, 1,0)
layout.addWidget(combosel, 1,1)
# Third row
layout.addWidget(labelbaud, 2,0)
layout.addWidget(combobaud, 2,1)
# Fourth row
layout.addWidget(buttonquit, 3,0)
layout.addWidget(buttonsync, 3,1)
# Fifth row
layout.addWidget(progressbar, 4,0,1,2)

window.setLayout(layout)
app.setStyle('Fusion')

# Routing to quit the application
def on_buttonquit_clicked():
    app.quit()
buttonquit.clicked.connect(on_buttonquit_clicked)

# Routine to discover system serial ports and populate the combo box
def get_serial():
    import serial.tools.list_ports
    ports = serial.tools.list_ports.comports(include_links=False)
    for port in ports :
        combosel.addItem(port.device)
get_serial()

# Routine to show a message that everything goes well
def all_done():
    alert = QMessageBox()
    alert.setText('La radio è stata sincronizzata !')
    alert.exec_()

def wait_zero():
    alert = QMessageBox()
    alert.setText('Attendo che i secondi siano 00 prima di sincronizzare, non chiudere la app fino messaggio di completamento !')
    alert.exec_()

# def advanceProgressBar():
#     curVal = progressbar.value()
#     maxVal = progressbar.maximum()
#     progressbar.setValue(curVal + (maxVal - curVal) / 100)

def sync_radio():
    import sys

    baudrate = str(combobaud.currentText())  # change to match your radio
    gmtoffset = 0  #change to a negative or positive offset from GMT if you
    #               want to use local time.  i.e. -5 for EST
    serialport = str(combosel.currentText()) # Serial port of your radios serial interface.
    baudratestr = str(baudrate)

    # Defining the command to set the radios time in hex bytes.
    preamble = ["0xFE", "0xFE", "0x94", "0xE0", "0x1A", "0x05", "0x00", "0x95"]
    postamble = "0xfd"
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
    wait_zero()

    lastsec = 1
    curVal = seconds
    while(seconds != 0):
        t = time.localtime()
        seconds = int(time.strftime("%S"))
        #maxVal = progressbar.maximum()
        maxVal = 60
        progressbar.maximum = maxVal
        curVal = seconds
        #progressbar.setValue(curVal + (maxVal - curVal) / 100)
        progressbar.setValue((curVal * 100)/ maxVal)
    if(seconds != lastsec):
            lastsec = seconds
    time.sleep(.01)

    progressbar.setValue = maxVal
    
    # Added by IW2NOY to synchronize also date with time
    preambledate = ["0xFE", "0xFE", "0x94", "0xE0", "0x1A", "0x05", "0x00", "0x95"]
    import datetime

    # Get today date
    from datetime import date
    today = date.today()
    year = today.strftime("%y")
    month = today.strftime("%m")
    day = today.strftime("%d")

    # Preparing hexcode for today date
    #preyear = "0x20" 
    year = "0x" + str(year)
    month = "0x" + str(month)
    day = "0x" + str(day)
    # print( year + " " + month + " " + day)

    #preambledate.append(preyear)
    preambledate.append(year)
    preambledate.append(month)
    preambledate.append(day)
    preambledate.append('0xFD')
    #print(" ")
    #print("Preamble date: " + str(preambledate))
    #print(" ")

    # End section for date

    # Now that we've reached the top of the minute, set the radios time!
    ser = serial.Serial(serialport, baudrate)

    count = 0
    while(count < 11):
        senddata = int(bytes(preamble[count], 'UTF-8'), 16)
        #Aggiunta di IW2NOY per debugging dei dati inviati
        #print ("Dati inviati a IC-7300 per l'orario al giro " + giro  + " : " + dati)
        #print ("Preamble:" + str(preamble))
        #Fine aggiunta
        ser.write(struct.pack('>B', senddata))
        count = count +1
    
    # Send date after time
    count = 0
    while(count < 12):
        senddata2 = int(bytes(preambledate[count], 'UTF-8'), 16)
        #Aggiunta di IW2NOY per debugging dei dati inviati
        #dati = str(senddata2)
        #giro = str(count)
        #print ("Dati inviati a IC-7300 per la data al giro " + giro  + " : " + dati)
        #print ("Preambledate:" + str(preambledate))
        #Fine aggiunta
        ser.write(struct.pack('>B', senddata2))
        count = count +1

    ser.close()
    all_done()
    # All done.  The radio is now in sync with the computer clock.

# Define buttons calls

buttonquit.clicked.connect(on_buttonquit_clicked)
buttonsync.clicked.connect(sync_radio)

# Finally show the windows GUI and run the application
window.show()
app.exec_()