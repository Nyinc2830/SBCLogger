
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Devices.InterfaceKit import InterfaceKit

import datetime
import sqlite3

def AttachInterfaceKit(databasepath, serialNumber):
	
       def inputChangeHandler(event):
	       conn = sqlite3.connect(databasepath)
	       conn.execute("INSERT INTO INTERFACEKIT_INPUTCHANGE VALUES(NULL, DateTime('now'), ?, ?, ?)", (event.device.getSerialNum(), event.index, event.state))
	       conn.commit()
	       conn.close()
       def outputChangeHandler(event):
	       conn = sqlite3.connect(databasepath)
	       conn.execute("INSERT INTO INTERFACEKIT_OUTPUTCHANGE VALUES(NULL, DateTime('now'), ?, ?, ?)", (event.device.getSerialNum(), event.index, event.state))
	       conn.commit()
	       conn.close()
       def sensorChangeHandler(event):
	       conn = sqlite3.connect(databasepath)
	       conn.execute("INSERT INTO INTERFACEKIT_SENSORCHANGE VALUES(NULL, DateTime('now'), ?, ?, ?)", (event.device.getSerialNum(), event.index, event.value))
	       conn.commit()
	       conn.close()
       try:
	       ik = InterfaceKit()
	       ik.setOnInputChangeHandler(inputChangeHandler)
	       ik.setOnOutputChangeHandler(outputChangeHandler)
	       ik.setOnSensorChangeHandler(sensorChangeHandler)
	       ik.openPhidget(serialNumber)
       except PhidgetException as e:
	       print("Phidget Exception %i: %s" % (e.code, e.details))
	       print("Exiting...")
	       exit(1)
#
	#print(serialNumber)
