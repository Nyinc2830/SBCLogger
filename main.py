__author__ = 'James Folk'
__version__ = '0.0.1'
__date__ = 'June 15 2016'

#Basic imports
from ctypes import *
import sys
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import SpatialDataEventArgs, AttachEventArgs, DetachEventArgs, ErrorEventArgs, TemperatureChangeEventArgs
from Phidgets.Devices.Spatial import Spatial, SpatialEventData, TimeSpan
from Phidgets.Phidget import Phidget
from Phidgets.Manager import Manager
from Phidgets.Phidget import PhidgetLogLevel
from Phidgets.Devices.InterfaceKit import InterfaceKit
from Phidgets.Devices.TemperatureSensor import TemperatureSensor, ThermocoupleType

import datetime
import sqlite3


databasepath = 'test.db'
loggingpath = 'phidgetlog.log'

def displayAttachedDeviceInfo(device):
	print("|------------|----------------------------------|--------------|------------|")
	print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
	print("|------------|----------------------------------|--------------|------------|")
	print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (device.isAttached(), device.getDeviceName(), device.getSerialNum(), device.getDeviceVersion()))
	print("|------------|----------------------------------|--------------|------------|")
			
def displayDetachedDeviceInfo(device):
	print("|------------|----------------------------------|--------------|------------|")
	print("|- Detached -|-              Type              -|- Serial No. -|-  Version -|")
	print("|------------|----------------------------------|--------------|------------|")
	print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (device.isAttached(), device.getDeviceName(), device.getSerialNum(), device.getDeviceVersion()))
	print("|------------|----------------------------------|--------------|------------|")

def displayErrorDeviceInfo(device):
	try:
		source = event.device
		print("GPS %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
	except PhidgetException as e:
		print("Phidget Exception %i: %s" % (e.code, e.details))

def createDB():

	conn = sqlite3.connect(databasepath)


	conn.execute('''CREATE TABLE IF NOT EXISTS PHIDGET_ATTACHED
	(ID INTEGER PRIMARY KEY AUTOINCREMENT,
	LOGTIME TIMESTAMP NOT NULL,
	SERIALNUMBER INT NOT NULL);''')

	conn.execute('''CREATE TABLE IF NOT EXISTS PHIDGET_DETACHED
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

	conn.commit()
	conn.close()

createDB()

def managerDeviceAttached(event):
	deviceClass = event.device.getDeviceClass()

	event.device.enableLogging(PhidgetLogLevel.PHIDGET_LOG_VERBOSE, loggingpath)

	deviceID = event.device.getDeviceID()
	deviceLabel = event.device.getDeviceLabel()
	deviceName = event.device.getDeviceName()
	deviceType = event.device.getDeviceType()
	deviceVersion = event.device.getDeviceVersion()
	deviceLibraryVersion = event.device.getLibraryVersion()
	deviceSerialNumber = event.device.getSerialNum()

	conn = sqlite3.connect(databasepath)
	conn.execute("INSERT INTO PHIDGET_ATTACHED(LOGTIME, SERIALNUMBER) \
			VALUES(DateTime('now'), %i)" % (event.device.getSerialNum()))
	conn.commit()
	conn.close()

	if deviceClass == 2:
		#attach accelerometer
		#ACCELEROMETER = 2        - Phidgets.Accelerometer
		print("Attach Accelerometer")
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
					VALUES(DateTime('now'), %i, %i, %i)" % (event.device.getSerialNum(), event.index, event.state))

			#event.device.getDataRate(event.index)
			#event.device.getDataRateMax(event.index)
			#event.device.getDataRateMin(event.index)
			#event.device.getInputCount()
			#event.device.getOutputCount()
			#event.getRatiometric()

			#conn.execute("INSERT OR REPLACE INTERFACEKIT(SERIALNUMBER, CLASS, ID, LABEL, NAME, TYPE, VERSION, LIBVERSION) \
			#		VALUES(%s, %s, %s, %s, %s, %i, %s)" % 
			#		(event.device.getSerialNum(), deviceID, deviceLabel, deviceName, deviceType, deviceVersion, deviceLibraryVersion))

			conn.commit()
			conn.close()
		def outputChangeHandler(event):
			conn = sqlite3.connect(databasepath)
			conn.execute("INSERT INTO INTERFACEKIT_OUTPUTCHANGE(LOGTIME, SERIALNUMBER, IDX, STATE) \
					VALUES(DateTime('now'), %i, %i, %i)" % (event.device.getSerialNum(), event.index, event.state))
			conn.commit()
			conn.close()
		def sensorChangeHandler(event):
			conn = sqlite3.connect(databasepath)
			conn.execute("INSERT INTO INTERFACEKIT_SENSORCHANGE(LOGTIME, SERIALNUMBER, IDX, VALUE) \
					VALUES(DateTime('now'), %i, %i, %i)" % (event.device.getSerialNum(), event.index, event.value))
			conn.commit()
			conn.close()
		try:
			ik = InterfaceKit()
			ik.setOnInputChangeHandler(inputChangeHandler)
			ik.setOnOutputChangeHandler(outputChangeHandler)
			ik.setOnSensorChangeHandler(sensorChangeHandler)
			ik.openPhidget(event.device.getSerialNum())
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
		print("Attach Spatial " + str(event.device.getSerialNum()))


		def onAttachHandler(event):
			logString = "Spatial Attached " + str(event.device.getSerialNum())
			print(logString)
			displayAttachedDeviceInfo(event.device)

		def onDetachHandler(event):
			logString = "Spatial Detached " + str(event.device.getSerialNum())
			print(logString)
			displayDetachedDeviceInfo(event.device)

			event.device.closePhidget()

		def onErrorHandler(event):
			logString = "Spatial Error " + str(event.device.getSerialNum()) + ", Error: " + event.description
			print(logString)
			displayErrorDeviceInfo(event.device)
			
		def onServerConnectHandler(event):
			logString = "Spatial Server Connect " + str(event.device.getSerialNum())
			print(logString)

		def onServerDisconnectHandler(event):
			logString = "Spatial Server Disconnect " + str(event.device.getSerialNum())
			print(logString)

		def spatialDataHandler(event):
			logString = "Spatial Changed " + str(event.device.getSerialNum())
			print(logString)

			conn = sqlite3.connect(databasepath)
				
			index = 0
			for spatialData in enumerate(event.spatialData):
				accelX = 0
				accelY = 0
				accelZ = 0
				if len(spatialData[1].Acceleration) > 0:
					accelX = spatialData[1].Acceleration[0]
					accelY = spatialData[1].Acceleration[1]
					if len(spatialData[1].Acceleration) > 2:
						accelZ = spatialData[1].Acceleration[2]

				angularX = 0
				angularY = 0
				angularZ = 0
				if len(spatialData[1].AngularRate) > 0:
					angularX = spatialData[1].AngularRate[0]
					angularY = spatialData[1].AngularRate[1]
					if len(spatialData[1].AngularRate) > 2:
						angularZ = spatialData[1].AngularRate[2]

				magneticX = 0
				magneticY = 0
				magneticZ = 0
				if len(spatialData[1].AngularRate) > 0:
					magneticX = spatialData[1].MagneticField[0]
					magneticY = spatialData[1].MagneticField[1]
					if len(spatialData[1].AngularRate) > 2:
						magneticZ = spatialData[1].MagneticField[2]

				#print(index)
				#print("Acceleration: " + str(spatialData[1].Acceleration))
				#print("AngularRate: " + str(spatialData[1].AngularRate))
				#print("MagneticField: " + str(spatialData[1].MagneticField))
				#print("Seconds: " + str(spatialData[1].Timestamp.seconds))
				conn.execute("INSERT INTO SPATIAL_DATACHANGE(LOGTIME, SERIALNUMBER, IDX, ACCELERATION_X, ACCELERATION_Y, ACCELERATION_Z, ANGULARRATE_X, ANGULARRATE_Y, ANGULARRATE_Z, MAGNETICFIELD_X, MAGNETICFIELD_Y, MAGNETICFIELD_X) VALUES(DateTime('now'), %i, %i, %f, %f, %f, %f, %f, %f, %f, %f, %f)" % (event.device.getSerialNum(), index, accelX, accelY, accelZ, angularX, angularY, angularZ, magneticX, magneticY, magneticZ))
				index += 1

			conn.commit()
			conn.close()

		try:
			p = Spatial()

			p.setOnAttachHandler(onAttachHandler)
			p.setOnDetachHandler(onDetachHandler)
			p.setOnErrorhandler(onErrorHandler)
			p.setOnServerConnectHandler(onServerConnectHandler)
			p.setOnServerDisconnectHandler(onServerDisconnectHandler)

			p.setOnSpatialDataHandler(spatialDataHandler)
			p.openPhidget(event.device.getSerialNum())
		except PhidgetException as e:
			print("Phidget Exception %i: %s" % (e.code, e.details))
			print("Exiting...")
			exit(1)

	elif deviceClass == 13:
		#attach stepper
		#STEPPER = 13             - Phidgets.Stepper
		print("Attach Stepper")
	elif deviceClass == 14:
		#attach temperature sensor
		#TEMPERATURESENSOR = 14   - Phidgets.TemperatureSensor
		print("Attach TemperatureSensor " + str(event.device.getSerialNum()))

		def onAttachHandler(event):
			print("Temperature Attached")

		def onDetachHandler(event):
			print("Temperature Detached")

		def onErrorHandler(event):
			print("Temperature Error: " + event.description)

		def onServerConnectHandler(event):
			print("Temperature Server Connect")

		def onServerDisconnectHandler(event):
			print("Temperature Server Disconnect")

		def temperatureChangeHandler(event):
			print("Temperature change")

			#conn = sqlite3.connect(databasepath)
			#index = event.index
			#temperature = event.temperature
			#potential = event.potential
			#
			#conn.execute("INSERT INTO TEMPERATURE_CHANGE(LOGTIME, SERIALNUMBER, IDX, TEMPERATURE, POTENTIAL) \
					#VALUES(DateTime('now'), %i, %i, %f, %f)" % (event.device.getSerialNum(), event.index, event.temperature, event.potential))
			#conn.commit()
			#conn.close()

		try:
			p = TemperatureSensor()
			p.setOnAttachHandler(onAttachHandler)
			p.setOnDetachHandler(onDetachHandler)
			p.setOnErrorhandler(onErrorHandler)
			p.setOnServerConnectHandler(onServerConnectHandler)
			p.setOnServerDisconnectHandler(onServerDisconnectHandler)

			p.setOnTemperatureChangeHandler(temperatureChangeHandler)
			p.openPhidget(event.device.getSerialNum())


			#p.waitForAttach(10000)

			#p.setThermocoupleType(0, ThermocoupleType.PHIDGET_TEMPERATURE_SENSOR_K_TYPE)
			#p.setTemperatureChangeTrigger(0, 0.10)

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
