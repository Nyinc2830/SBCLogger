__author__ = 'James Folk'
__version__ = '0.0.1'
__date__ = 'June 15 2016'

#Basic imports
from ctypes import *
import sys
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs
from Phidgets.Phidget import Phidget
from Phidgets.Manager import Manager
from Phidgets.Phidget import PhidgetLogLevel
from Phidgets.Devices.InterfaceKit import InterfaceKit

import datetime
import sqlite3


databasepath = 'test.db'

def createDB():

	conn = sqlite3.connect(databasepath)


	conn.execute('''CREATE TABLE PHIDGET_ATTACHED
	(ID INTEGER PRIMARY KEY AUTOINCREMENT,
	LOGTIME TIMESTAMP NOT NULL,
	SERIALNUMBER INT NOT NULL);''')

	conn.execute('''CREATE TABLE PHIDGET_DETACHED
	(ID INTEGER PRIMARY KEY AUTOINCREMENT,
	LOGTIME TIMESTAMP NOT NULL,
	SERIALNUMBER INT NOT NULL);''')

##########################################################################

	#event.device.getDataRate(event.index)
	#event.device.getDataRateMax(event.index)
	#event.device.getDataRateMin(event.index)
	#event.device.getInputCount()
	#event.device.getOutputCount()
	#event.getRatiometric()

	#conn.execute('''CREATE TABLE INTERFACEKIT
	#(SERIALNUMBER INTEGER PRIMARY KEY,
	#CLASS CHAR(50),
	#ID CHAR(50),
	#LABEL CHAR(50),
	#NAME CHAR(50),
	#TYPE CHAR(50),
	#VERSION INT,
	#LIBVERSION CHAR(50),
	#DATARATE);''');

	conn.execute('''CREATE TABLE INTERFACEKIT_INPUTCHANGE
	(ID INTEGER PRIMARY KEY AUTOINCREMENT,
	LOGTIME TIMESTAMP NOT NULL,
	SERIALNUMBER INT NOT NULL,
	IDX INT,
	STATE INT);''')

	conn.execute('''CREATE TABLE INTERFACEKIT_OUTPUTCHANGE
	(ID INTEGER PRIMARY KEY AUTOINCREMENT,
	LOGTIME TIMESTAMP NOT NULL,
	SERIALNUMBER INT NOT NULL,
	IDX INT,
	STATE INT);''')

	conn.execute('''CREATE TABLE INTERFACEKIT_SENSORCHANGE
	(ID INTEGER PRIMARY KEY AUTOINCREMENT,
	LOGTIME TIMESTAMP NOT NULL,
	SERIALNUMBER INT NOT NULL,
	IDX INT,
	VALUE INT);''')

############################################################################

	conn.commit()
	conn.close()

createDB()

def managerDeviceAttached(event):
	deviceClass = event.device.getDeviceClass()

	deviceID = event.device.getDeviceID()
	deviceLabel = event.device.getDeviceLabel()
	deviceName = event.device.getDeviceName()
	deviceType = event.device.getDeviceType()
	deviceVersion = event.device.getDeviceVersion()
	deviceLibraryVersion = event.device.getLibraryVersion()
	deviceSerialNumber = event.device.getSerialNum()

	conn = sqlite3.connect(databasepath)
	conn.execute("INSERT INTO PHIDGET_ATTACHED(LOGTIME, SERIALNUMBER) \
			VALUES(DateTime('now'), %i)" % (deviceSerialNumber))
	conn.commit()
	conn.close()

	if deviceClass == 2:
		#attach accelerometer
		#ACCELEROMETER = 2        - Phidgets.Accelerometer
		print("Attach Accelerometer")

		def accelChangeHandler(event):
			conn = sqlite3.connect(databasepath)
			conn.execute("INSERT INTO ACCELEROMETER_CHANGE(LOGTIME, SERIALNUMBER, IDX, ACCELERATION) \
					VALUES(DateTime('now'), %i, %i, %i)" % (deviceSerialNumber, event.index, event.acceleration))
			conn.commit()
			conn.close()
		try:
			p = Accelerometer()
			p.setOnAccelerationChangeHandler(accelChangeHandler)
			p.openPhidget(deviceSerialNumber)
		except PhidgetException as e:
			print("Phidget Exception %i: %s" % (e.code, e.details))
			print("Exiting...")
			exit(1)
	elif deviceClass == 3:
		#attach advancedservo
		#ADVANCEDSERVO = 3        - Phidgets.AdvanceServo
		print("Attach AdvanceServo")
	elif deviceClass == 22:
		#attach analog
		#ANALOG = 22              - Phidgets.Analog
		print("Attach Analog")
	elif deviceClass == 23:
		#attach bridge
		#BRIDGE = 23              - Phidgets.Bridge
		print("Attach Bridge")
	elif deviceClass == 4:
		#attach encoder
		#ENCODER = 4              - Phidgets.Encoder
		print("Attach Encoder")
	elif deviceClass == 21:
		#attach frequency counter
		#FREQUENCYCOUNTER = 21    - Phidgets.FrequencyCounter
		print("Attach FrequencyCounter")
	elif deviceClass == 5:
		#attach gps
		#GPS = 5                  - Phidgets.GPS
		print("Attach GPS")
	elif deviceClass == 7:
		#attach interface kit
		#INTERFACEKIT = 7         - Phidgets.InterfaceKit 
		
		print("Attach InterfaceKit")

		def inputChangeHandler(event):
			conn = sqlite3.connect(databasepath)
			conn.execute("INSERT INTO INTERFACEKIT_INPUTCHANGE(LOGTIME, SERIALNUMBER, IDX, STATE) \
					VALUES(DateTime('now'), %i, %i, %i)" % (deviceSerialNumber, event.index, event.state))

			#event.device.getDataRate(event.index)
			#event.device.getDataRateMax(event.index)
			#event.device.getDataRateMin(event.index)
			#event.device.getInputCount()
			#event.device.getOutputCount()
			#event.getRatiometric()

			#conn.execute("INSERT OR REPLACE INTERFACEKIT(SERIALNUMBER, CLASS, ID, LABEL, NAME, TYPE, VERSION, LIBVERSION) \
			#		VALUES(%s, %s, %s, %s, %s, %i, %s)" % 
			#		(deviceSerialNumber, deviceID, deviceLabel, deviceName, deviceType, deviceVersion, deviceLibraryVersion))

			conn.commit()
			conn.close()
		def outputChangeHandler(event):
			conn = sqlite3.connect(databasepath)
			conn.execute("INSERT INTO INTERFACEKIT_OUTPUTCHANGE(LOGTIME, SERIALNUMBER, IDX, STATE) \
					VALUES(DateTime('now'), %i, %i, %i)" % (deviceSerialNumber, event.index, event.state))
			conn.commit()
			conn.close()
		def sensorChangeHandler(event):
			conn = sqlite3.connect(databasepath)
			conn.execute("INSERT INTO INTERFACEKIT_SENSORCHANGE(LOGTIME, SERIALNUMBER, IDX, VALUE) \
					VALUES(DateTime('now'), %i, %i, %i)" % (deviceSerialNumber, event.index, event.value))
			conn.commit()
			conn.close()
		try:
			ik = InterfaceKit()
			ik.setOnInputChangeHandler(inputChangeHandler)
			ik.setOnOutputChangeHandler(outputChangeHandler)
			ik.setOnSensorChangeHandler(sensorChangeHandler)
			ik.openPhidget(deviceSerialNumber)
		except PhidgetException as e:
			print("Phidget Exception %i: %s" % (e.code, e.details))
			print("Exiting...")
			exit(1)

	elif deviceClass == 19:
		#attach ir
		#IR = 19                  - Phidgets.IR
		print("Attach IR")
	elif deviceClass == 8:
		#attach led
		#LED = 8                  - Phidgets.LED
		print("Attach LED")
	elif deviceClass == 9:
		#attach motorcontrol
		#MOTORCONTROL = 9         - Phidgets.MotorControl
		print("Attach MotorControl")
	elif deviceClass == 1:
		#attach nothing
		#NOTHING = 1
		print("Attach Nothing")
	elif deviceClass == 10:
		#attach phsensor
		#PHSENSOR = 10            - Phidgets.PHSensor
		print("Attach PHSensor")
	elif deviceClass == 11:
		#attach rfid
		#RFID = 11                - Phidgets.RFID
		print("Attach RFID")
	elif deviceClass == 12:
		#attach servo
		#SERVO = 12               - Phidgets.Servo
		print("Attach Servo")
	elif deviceClass == 20:
		#attach spatial
		#SPATIAL = 20             - Phidgets.Spatial
		print("Attach Spatial")
	elif deviceClass == 13:
		#attach stepper
		#STEPPER = 13             - Phidgets.Stepper
		print("Attach Stepper")
	elif deviceClass == 14:
		#attach temperature sensor
		#TEMPERATURESENSOR = 14   - Phidgets.TemperatureSensor
		print("Attach TemperatureSensor")

		def temperatureChangeHandler(event):
			conn = sqlite3.connect(databasepath)
			index = event.index
			temperature = event.temperature
			potential = event.potential
			
			conn.execute("INSERT INTO TEMPERATURE_CHANGE(LOGTIME, SERIALNUMBER, IDX, TEMPERATURE, POTENTIAL) \
					VALUES(DateTime('now'), %i, %i, %f, %f)" % (deviceSerialNumber, event.index, event.temperature, event.potential))
			conn.commit()
			conn.close()
		try:
			p = TemperatureSensor()
			p.setOnTemperatureChangeHandler(temperatureChangeHandler)
			p.openPhidget(deviceSerialNumber)
		except PhidgetException as e:
			print("Phidget Exception %i: %s" % (e.code, e.details))
			print("Exiting...")
			exit(1)
	elif deviceClass == 15:
		#attach textlcd
		#TEXTLCD = 15             - Phidgets.TextLCD
		print("Attach TextLCD")
	elif deviceClass == 16:
		#attach textled
		print("TEXTLED not supported")
	elif deviceClass == 17:
		#attach weight sensor
		print("WEIGHTSENSOR not supported")

	#TEXTLED = 16
	#WEIGHTSENSOR = 17
	

def managerDeviceDetached(event):
	conn = sqlite3.connect(databasepath)
	conn.execute("INSERT INTO PHIDGET_DETACHED(LOGTIME, SERIALNUMBER) \
			VALUES(DateTime('now'), %i)" % (event.device.getSerialNum()))
	conn.commit()
	conn.close()

def managerErrorHandler(event):
	device = event.device
	description = event.description
	eCode = event.eCode
	print("Manager - Device %i: %s Error! (%d: %s)" % (detached.getSerialNum(), detached.getDeviceName(), eCode, description))

def managerServerConnect(event):
	device = event.device
	print("Manager - Device %i: %s Connected!" % (device.getSerialNum(), device.getDeviceName()))

def managerServerDisconnect(event):
	device = event.device
	print("Manager - Device %i: %s Disconnected!" % (device.getSerialNum(), device.getDeviceName()))


def main():
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
