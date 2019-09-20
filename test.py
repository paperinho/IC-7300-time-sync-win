#!/d/Python/Python37/python

# import sys

# print ("Number of arguments:", len(sys.argv), "arguments.")
# print ("Argument List:" , str(sys.argv))
# print ("")
# print (sys.argv[1])
# print (sys.argv[2])


# Teste datetime
import datetime

from datetime import date
today = date.today()
newtoday = today.strftime("%y%m%d")
print("Today's date:", today)
print("NewToday's date:", newtoday)