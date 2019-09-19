# IC-7300-time-sync-args
Python3 script to sync the radio's clock with your computer via CAT commands.
Originally written by Kevin Loughin KB9RLW in Python for Linux and now modified to run on Windows like an EXE.

The script, now and EXE, also accept parameters on command line instead of modify the variables valus inside.

You can run it manually from the terminal (cmd.exE), or set it up as a scheduled task to automatically update the radio clock at an interval.  

After downloading the script, you can run it as executable.  

From most desktops, you can right-click on the EXE and create a shortcut on the desktop and next you can select properties and in the "Destination" field insert the two paramters required (baud speed and COM port). In this way, you can also run the program with a classic 
double-click from your desktop.

When run, the script will get the current time of your computer, wait for the top of the minute at 00 seconds, and set the radio's time.

Thanks to Kevin Loughin - KB9RLW for the solution and the initial effort.

-Graziano IW2NOY-
