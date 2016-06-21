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

		def accelChangeHandler(event):
			conn = sqlite3.connect(databasepath)
			conn.execute("INSERT INTO ACCELEROMETER_CHANGE(LOGTIME, SERIALNUMBER, IDX, ACCELERATION) \
					VALUES(DateTime('now'), %i, %i, %i)" % (event.device.getSerialNum(), event.index, event.acceleration))
			conn.commit()
			conn.close()
		try:
			p = Accelerometer()
			p.setOnAccelerationChangeHandler(accelChangeHandler)
			p.openPhidget(event.device.getSerialNum())
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
			print("Spatial Attached")

		def onDetachHandler(event):
			print("Spatial Detached")
			event.device.closePhidget()

		def onErrorHandler(event):
			print("Spatial Error: " + event.description)

		def onServerConnectHandler(event):
			print("Spatial Server Connect")

		def onServerDisconnectHandler(event):
			print("Spatial Server Disconnect")


		def spatialDataHandler(event):
			print("Spatial changed")
			for spatialData in enumerate(event.spatialData):
				print(spatialData[1].Acceleration)
				print(spatialData[1].AngularRate)
				print(spatialData[1].MagneticField)
				print(spatialData[1].Timestamp.seconds)

			#print(event.device.getAccelerationAxisCount())
			#print(event.device.getCompassAxisCount())
			#print(event.device.getGyroAxisCount())

			acceleration = []
			#for i in range(0, event.device.getAccelerationAxisCount()):
				#acceleration.append(event.device.getAcceleration(i))

			#compass = []
			#for i in range(0, event.device.getCompassAxisCount()):
				#compass.append(event.device.getMagneticField(i))
			
			#gyro = []
			#for i in range(0, event.device.getGyroAxisCount()):
				#gyro.append(event.device.getAngularRate(i))

			#print(len(event.spatialData))
			#print(event.spatialData[0].acceleration)
			#print(event.spatialData[0])
			#print(event.spatialData[0])


			#print(compass)
			#print(acceleration)
			#print(gyro)
			#print("------------------------------------------")

			#source = event.device
			##DisplayDeviceInfo(event.device)
			#print("Spatial %i: Amount of data %i" % (source.getSerialNum(), len(event.spatialData)))
			#for spatialData in event.spatialData:
				#print(len(spatialData.Acceleration))
				#print(len(spatialData.AngularRate))
				#print(len(spatialData.MagneticField))
				#print(len(spatialData.TimeStamp))
			#for index, spatialData in enumerate(event.spatialData):
				#print("=== Data Set: %i ===" % (index))
				#if len(spatialData.Acceleration) > 0:
					#print("Acceleration> x: %6f  y: %6f  z: %6f" % (spatialData.Acceleration[0], spatialData.Acceleration[1], spatialData.Acceleration[2]))
				#if len(spatialData.AngularRate) > 0:
					#print("Angular Rate> x: %6f  y: %6f  z: %6f" % (spatialData.AngularRate[0], spatialData.AngularRate[1], spatialData.AngularRate[2]))
				#if len(spatialData.MagneticField) > 0:
					#print("Magnetic Field> x: %6f  y: %6f  z: %6f" % (spatialData.MagneticField[0], spatialData.MagneticField[1], spatialData.MagneticField[2]))
				#print("Time Span> Seconds Elapsed: %i  microseconds since last packet: %i" % (spatialData.Timestamp.seconds, spatialData.Timestamp.microSeconds))
#
			#print("------------------------------------------")

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
