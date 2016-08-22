
from DeviceInfo import DisplayAttachedDeviceInfo
from DeviceInfo import DisplayDetachedDeviceInfo
from DeviceInfo import DisplayErrorDeviceInfo

from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException

from Phidgets.Events.Events import GPSPositionChangeEventArgs, PositionChangeEventArgs, InputChangeEventArgs, AttachEventArgs, DetachEventArgs, ErrorEventArgs
from Phidgets.Devices.GPS import GPS

import datetime
import sqlite3

def AttachGPS(databasepath, serialNumber):
	def onAttachHandler(event):
		logString = "GPS Attached " + str(event.device.getSerialNum())
		#print(logString)
		DisplayAttachedDeviceInfo(event.device)

	def onDetachHandler(event):
		logString = "GPS Detached " + str(event.device.getSerialNum())
		#print(logString)
		DisplayDetachedDeviceInfo(event.device)

		event.device.closePhidget()

	def onErrorHandler(event):
		logString = "GPS Error " + str(event.device.getSerialNum()) + ", Error: " + event.description
		print(logString)

		DisplayErrorDeviceInfo(event.device)
		
	def onServerConnectHandler(event):
		logString = "GPS Server Connect " + str(event.device.getSerialNum())
		#print(logString)

	def onServerDisconnectHandler(event):
		logString = "GPS Server Disconnect " + str(event.device.getSerialNum())
		#print(logString)

	def positionChangeHandler(event):
		logString = "GPS Position Changed"
		#print(logString)

		try:
			conn = sqlite3.connect(databasepath)

			conn.execute("INSERT INTO GPS_POSITIONCHANGE VALUES(NULL, DateTime('now'), ?, ?, ?)",
					(event.device.getSerialNum(), event.index, event.position))

			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

	def positionFixStatusChangeHandler(event):
		logString = "GPS Position Fix Status Changed"
		#print(logString)

		try:
			conn = sqlite3.connect(databasepath)

			conn.execute("INSERT INTO GPS_POSITIONFIXSTATUSCHANGE VALUES(NULL, DateTime('now'), ?, ?, ?)",
					(event.device.getSerialNum(), event.index, event.position))

			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

	try:
		p = GPS()

		p.setOnAttachHandler(onAttachHandler)
		p.setOnDetachHandler(onDetachHandler)
		p.setOnErrorhandler(onErrorHandler)
		p.setOnServerConnectHandler(onServerConnectHandler)
		p.setOnServerDisconnectHandler(onServerDisconnectHandler)

		p.setOnPositionChangeHandler(positionChangeHandler)
		p.setOnPositionFixStatusChangeHandler(positionFixStatusChangeHandler)

		p.openPhidget(serialNumber)

	except PhidgetException as e:
		print("Phidget Exception %i: %s" % (e.code, e.details))
		print("Exiting...")
		exit(1)

