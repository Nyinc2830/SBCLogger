__author__ = 'James Folk'
__version__ = '0.0.1'
__date__ = 'June 15 2016'

#Basic imports
from ctypes import *
import sys

#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import SpatialDataEventArgs, AttachEventArgs, DetachEventArgs, ErrorEventArgs, TemperatureChangeEventArgs
from Phidgets.Phidget import Phidget
from Phidgets.Manager import Manager
from Phidgets.Phidget import PhidgetLogLevel

import datetime
import sqlite3

from InterfaceKit import AttachInterfaceKit
from Spatial import AttachSpatial
from Temperature import AttachTemperature
from Accelerometer import AttachAccelerometer

databasepath = '/usr/data/test.db'
loggingpath = 'phidgetlog.log'


def createDB():

	try:
		conn = sqlite3.connect(databasepath)

		conn.execute('''CREATE TABLE IF NOT EXISTS PHIDGET_ATTACHED
		(ID INTEGER PRIMARY KEY AUTOINCREMENT,
		LOGTIME TIMESTAMP NOT NULL,
		SERIALNUMBER INT NOT NULL);''')

		conn.execute('''CREATE TABLE IF NOT EXISTS PHIDGET_DETACHED
		(ID INTEGER PRIMARY KEY AUTOINCREMENT,
		LOGTIME TIMESTAMP NOT NULL,
		SERIALNUMBER INT NOT NULL);''')

		conn.execute('''CREATE TABLE IF NOT EXISTS PHIDGET_ERROR
		(ID INTEGER PRIMARY KEY AUTOINCREMENT,
		LOGTIME TIMESTAMP NOT NULL,
		SERIALNUMBER INT NOT NULL,
		CODE INT NOT NULL,
		DESCRIPTION CHAR(512) NOT NULL);''')

##########################################################################

		conn.execute('''CREATE TABLE IF NOT EXISTS INTERFACEKIT_INPUTCHANGE
		(ID INTEGER PRIMARY KEY AUTOINCREMENT,
		LOGTIME TIMESTAMP NOT NULL,
		SERIALNUMBER INT NOT NULL,
		IDX INT,
		STATE INT);''')

		conn.execute('''CREATE TABLE IF NOT EXISTS INTERFACEKIT_OUTPUTCHANGE
		(ID INTEGER PRIMARY KEY AUTOINCREMENT,
		LOGTIME TIMESTAMP NOT NULL,
		SERIALNUMBER INT NOT NULL,
		IDX INT,
		STATE INT);''')

		conn.execute('''CREATE TABLE IF NOT EXISTS INTERFACEKIT_SENSORCHANGE
		(ID INTEGER PRIMARY KEY AUTOINCREMENT,
		LOGTIME TIMESTAMP NOT NULL,
		SERIALNUMBER INT NOT NULL,
		IDX INT,
		VALUE INT);''')

############################################################################

		conn.execute('''CREATE TABLE IF NOT EXISTS SPATIAL_DATACHANGE
		(ID INTEGER PRIMARY KEY AUTOINCREMENT,
		LOGTIME TIMESTAMP NOT NULL,
		SERIALNUMBER INT NOT NULL,
		IDX INT,
		ACCELERATION_X REAL,
		ACCELERATION_Y REAL,
		ACCELERATION_Z REAL,
		ANGULARRATE_X REAL,
		ANGULARRATE_Y REAL,
		ANGULARRATE_Z REAL,
		MAGNETICFIELD_X REAL,
		MAGNETICFIELD_Y REAL,
		MAGNETICFIELD_Z REAL);''')

##########################################################################

		conn.execute('''CREATE TABLE IF NOT EXISTS TEMPERATURE_CHANGE
		(ID INTEGER PRIMARY KEY AUTOINCREMENT,
		LOGTIME TIMESTAMP NOT NULL,
		SERIALNUMBER INT NOT NULL,
		IDX INT,
		TEMPERATURE REAL,
		POTENTIAL REAL);''')

##########################################################################

		conn.execute('''CREATE TABLE IF NOT EXISTS ACCELEROMETER_CHANGE
		(ID INTEGER PRIMARY KEY AUTOINCREMENT,
		LOGTIME TIMESTAMP NOT NULL,
		SERIALNUMBER INT NOT NULL,
		IDX INT,
		ACCELERATION REAL);''')

##########################################################################
		conn.commit()
		conn.close()
	except sqlite3.Error as e:
		print "An error occurred:", e.args[0]

def managerDeviceAttached(event):
	deviceClass = event.device.getDeviceClass()

	event.device.enableLogging(PhidgetLogLevel.PHIDGET_LOG_VERBOSE, loggingpath)

	try:
		conn = sqlite3.connect(databasepath)
		conn.execute("INSERT INTO PHIDGET_ATTACHED(LOGTIME, SERIALNUMBER) \
				VALUES(DateTime('now'), %i)" % (event.device.getSerialNum()))
		conn.commit()
		conn.close()
	except sqlite3.Error as e:
		print "An error occurred:", e.args[0]


	if   deviceClass ==  2:AttachAccelerometer(databasepath, event.device.getSerialNum())
	elif deviceClass ==  3:print("Attach AdvanceServo")
	elif deviceClass == 22:print("Attach Analog")
	elif deviceClass == 23:print("Attach Bridge")
	elif deviceClass ==  4:print("Attach Encoder")
	elif deviceClass == 21:print("Attach FrequencyCounter")
	elif deviceClass ==  5:print("Attach GPS")
	elif deviceClass ==  7:AttachInterfaceKit(databasepath, event.device.getSerialNum())
	elif deviceClass == 19:print("Attach IR")
	elif deviceClass ==  8:print("Attach LED")
	elif deviceClass ==  9:print("Attach MotorControl")
	elif deviceClass ==  1:print("Attach Nothing")
	elif deviceClass == 10:print("Attach PHSensor")
	elif deviceClass == 11:print("Attach RFID")
	elif deviceClass == 12:print("Attach Servo")
	elif deviceClass == 20:AttachSpatial(databasepath, event.device.getSerialNum())
	elif deviceClass == 13:print("Attach Stepper")
	elif deviceClass == 14:AttachTemperature(databasepath, event.device.getSerialNum())
	elif deviceClass == 15:print("Attach TextLCD")
	elif deviceClass == 16:print("TEXTLED not supported")
	elif deviceClass == 17:print("WEIGHTSENSOR not supported")
	#TEXTLED = 16
	#WEIGHTSENSOR = 17
	

def managerDeviceDetached(event):
	try:
		conn = sqlite3.connect(databasepath)
		conn.execute("INSERT INTO PHIDGET_DETACHED(LOGTIME, SERIALNUMBER) \
				VALUES(DateTime('now'), %i)" % (event.device.getSerialNum()))
		conn.commit()
		conn.close()
	except sqlite3.Error as e:
		print "An error occurred:", e.args[0]

def managerErrorHandler(event):
	device = event.device
	description = event.description
	eCode = event.eCode
	try:
		conn = sqlite3.connect(databasepath)
		conn.execute("INSERT INTO PHIDGET_ERROR(LOGTIME, SERIALNUMBER, CODE, DESCRIPTION) \
				VALUES(DateTime('now'), %i, %i, %s)" % (event.device.getSerialNum(), event.eCode, event.description))
		conn.commit()
		conn.close()
	except sqlite3.Error as e:
		print "An error occurred:", e.args[0]

def managerServerConnect(event):
	device = event.device
	print("Manager - Device %i: %s Connected!" % (device.getSerialNum(), device.getDeviceName()))

def managerServerDisconnect(event):
	device = event.device
	print("Manager - Device %i: %s Disconnected!" % (device.getSerialNum(), device.getDeviceName()))


def main():
	createDB()

	try:
		manager = Manager()
	except RuntimeError as e:
		print("RuntimeException: %s" % e.details)
		print("Exiting...")
		exit(1)

	try:
		manager.setOnAttachHandler(managerDeviceAttached)
		manager.setOnDetachHandler(managerDeviceDetached)
		manager.setOnErrorHandler(managerErrorHandler)
		manager.setOnServerConnectHandler(managerServerConnect)
		manager.setOnServerDisconnectHandler(managerServerDisconnect)
		manager.openManager()

	except PhidgetException as e:
		print("Phidget Exception %i: %s" % (e.code, e.details))
		print("Exiting...")
		exit(1)
	try:
		manager.openManager()
	except PhidgetException as e:
		print("Phidget Exception %i: %s" % (e.code, e.details))
		print("Exiting...")
		exit(1)

	print("Press Enter to quit...")
	chr = sys.stdin.read(1)
	print("Closing...")

	try:
		manager.closeManager()
	except PhidgetException as e:
		print("Phidget Exception %i: %s" % (e.code, e.details))
		print("Exiting...")
		exit(1)
	print("Done.")
	exit(0)


if __name__ == "__main__":
	main()
