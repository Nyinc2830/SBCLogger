
from DeviceInfo import DisplayAttachedDeviceInfo
from DeviceInfo import DisplayDetachedDeviceInfo
from DeviceInfo import DisplayErrorDeviceInfo

from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AccelerationChangeEventArgs, AttachEventArgs, DetachEventArgs, ErrorEventArgs
from Phidgets.Devices.Accelerometer import Accelerometer

import datetime
import sqlite3

def AttachAccelerometer(databasepath, serialNumber):
	def onAttachHandler(event):
		logString = "Accelerometer Attached " + str(event.device.getSerialNum())
		#print(logString)
		DisplayAttachedDeviceInfo(event.device)

	def onDetachHandler(event):
		logString = "Accelerometer Detached " + str(event.device.getSerialNum())
		#print(logString)
		DisplayDetachedDeviceInfo(event.device)

		event.device.closePhidget()

	def onErrorHandler(event):
		logString = "Accelerometer Error " + str(event.device.getSerialNum()) + ", Error: " + event.description
		#print(logString)
		DisplayErrorDeviceInfo(event)
		
	def onServerConnectHandler(event):
		logString = "Accelerometer Server Connect " + str(event.device.getSerialNum())
		#print(logString)

	def onServerDisconnectHandler(event):
		logString = "Accelerometer Server Disconnect " + str(event.device.getSerialNum())
		#print(logString)

	def accelerationChangeHandler(event):
		logString = "Accelerometer Changed " + str(event.device.getSerialNum())
		#print(logString)

		sqliteStatement = "INSERT INTO ACCELEROMETER_CHANGE(LOGTIME, SERIALNUMBER, IDX, ACCELERATION) VALUES(DateTime('now'), %i, %i, %f)" % (event.device.getSerialNum(), event.index, event.acceleration)
		try:
			conn = sqlite3.connect(databasepath)
			conn.execute(sqliteStatement)
			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]
	try:
		p = Accelerometer()

		p.setOnAttachHandler(onAttachHandler)
		p.setOnDetachHandler(onDetachHandler)
		p.setOnErrorhandler(onErrorHandler)
		p.setOnServerConnectHandler(onServerConnectHandler)
		p.setOnServerDisconnectHandler(onServerDisconnectHandler)

		p.setOnAccelerationChangeHandler(accelerationChangeHandler)
		p.openPhidget(serialNumber)

	except PhidgetException as e:
		print("Phidget Exception %i: %s" % (e.code, e.details))
		print("Exiting...")
		exit(1)

