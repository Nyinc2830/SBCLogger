
from DeviceInfo import DisplayAttachedDeviceInfo
from DeviceInfo import DisplayDetachedDeviceInfo
from DeviceInfo import DisplayErrorDeviceInfo

from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AccelerationChangeEventArgs, AttachEventArgs, DetachEventArgs, ErrorEventArgs
from Phidgets.Devices.RFID import RFID, RFIDTagProtocol

import datetime
import sqlite3

def AttachRFID(databasepath, serialNumber):
	def onAttachHandler(event):
		logString = "RFID Attached " + str(event.device.getSerialNum())
		#print(logString)
		DisplayAttachedDeviceInfo(event.device)

	def onDetachHandler(event):
		logString = "RFID Detached " + str(event.device.getSerialNum())
		#print(logString)
		DisplayDetachedDeviceInfo(event.device)

		event.device.closePhidget()

	def onErrorHandler(event):
		logString = "RFID Error " + str(event.device.getSerialNum()) + ", Error: " + event.description
		#print(logString)
		DisplayErrorDeviceInfo(event)
		
	def onServerConnectHandler(event):
		logString = "RFID Server Connect " + str(event.device.getSerialNum())
		#print(logString)

	def onServerDisconnectHandler(event):
		logString = "RFID Server Disconnect " + str(event.device.getSerialNum())
		#print(logString)


	def outputChangeHandler(event):
		logString = "RFID Changed " + str(event.device.getSerialNum())
		#print(logString)

		try:
			conn = sqlite3.connect(databasepath)
			conn.execute("INSERT INTO RFID_OUTPUTCHANGE VALUES(NULL, DateTime('now'), ?, ?, ?)", 
					(event.device.getSerialNum(), event.index, event.value))
			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

	def tagHandler(event):
		logString = "RFID Changed " + str(event.device.getSerialNum())
		#print(logString)

		try:
			conn = sqlite3.connect(databasepath)

			conn.execute("INSERT INTO RFID_TAG VALUES(NULL, DateTime('now'), ?, ?)", 
					(event.device.getSerialNum(), event.tag))

			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

	def tagLostHandler(event):
		logString = "RFID Changed " + str(event.device.getSerialNum())
		#print(logString)

		try:
			conn = sqlite3.connect(databasepath)

			conn.execute("INSERT INTO RFID_TAGLOST VALUES(NULL, DateTime('now'), ?, ?)", 
					(event.device.getSerialNum(), event.tag))

			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

	def accelerationChangeHandler(event):
		logString = "RFID Changed " + str(event.device.getSerialNum())
		#print(logString)

		try:
			conn = sqlite3.connect(databasepath)
			conn.execute("INSERT INTO ACCELEROMETER_CHANGE VALUES(NULL, DateTime('now'), ?, ?, ?)", 
					(event.device.getSerialNum(), event.index, event.acceleration))
			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]
	try:
		p = RFID()

		p.setOnAttachHandler(onAttachHandler)
		p.setOnDetachHandler(onDetachHandler)
		p.setOnErrorhandler(onErrorHandler)
		p.setOnServerConnectHandler(onServerConnectHandler)
		p.setOnServerDisconnectHandler(onServerDisconnectHandler)

		p.setOnOutputChangeHandler(outputChangeHandler)
		p.setOnTagHandler         (tagHandler)
		p.setOnTagLostHandler     (tagLostHandler)

		p.openPhidget(serialNumber)

	except PhidgetException as e:
		print("Phidget Exception %i: %s" % (e.code, e.details))
		print("Exiting...")
		exit(1)

