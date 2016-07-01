
from DeviceInfo import DisplayAttachedDeviceInfo
from DeviceInfo import DisplayDetachedDeviceInfo
from DeviceInfo import DisplayErrorDeviceInfo

from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import TemperatureChangeEventArgs, AttachEventArgs, DetachEventArgs, ErrorEventArgs
from Phidgets.Devices.TemperatureSensor import TemperatureSensor, ThermocoupleType

import datetime
import sqlite3

def AttachTemperature(databasepath, serialNumber):
	def onAttachHandler(event):
		logString = "Temperature Attached " + str(event.device.getSerialNum())
		#print(logString)
		DisplayAttachedDeviceInfo(event.device)

	def onDetachHandler(event):
		logString = "Temperature Detached " + str(event.device.getSerialNum())
		#print(logString)
		DisplayDetachedDeviceInfo(event.device)

		event.device.closePhidget()

	def onErrorHandler(event):
		logString = "Temperature Error " + str(event.device.getSerialNum()) + ", Error: " + event.description
		#print(logString)
		DisplayErrorDeviceInfo(event)
		
	def onServerConnectHandler(event):
		logString = "Temperature Server Connect " + str(event.device.getSerialNum())
		#print(logString)

	def onServerDisconnectHandler(event):
		logString = "Temperature Server Disconnect " + str(event.device.getSerialNum())
		#print(logString)

	def temperatureChangeHandler(event):
		logString = "Temperature Changed " + str(event.device.getSerialNum())
		sqliteStatement = "INSERT INTO TEMPERATURE_CHANGE(LOGTIME, SERIALNUMBER, IDX, TEMPERATURE, POTENTIAL) VALUES(DateTime('now'), %i, %i, %f, %f)" % (event.device.getSerialNum(), event.index, event.temperature, event.potential)
		try:
			conn = sqlite3.connect(databasepath)
			conn.execute(sqliteStatement)
			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]
	try:
		p = TemperatureSensor()

		p.setOnAttachHandler(onAttachHandler)
		p.setOnDetachHandler(onDetachHandler)
		p.setOnErrorhandler(onErrorHandler)
		p.setOnServerConnectHandler(onServerConnectHandler)
		p.setOnServerDisconnectHandler(onServerDisconnectHandler)

		p.setOnTemperatureChangeHandler(temperatureChangeHandler)
		p.openPhidget(serialNumber)

	except PhidgetException as e:
		print("Phidget Exception %i: %s" % (e.code, e.details))
		print("Exiting...")
		exit(1)

