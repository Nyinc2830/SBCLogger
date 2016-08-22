
from DeviceInfo import DisplayAttachedDeviceInfo
from DeviceInfo import DisplayDetachedDeviceInfo
from DeviceInfo import DisplayErrorDeviceInfo

from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException

from Phidgets.Events.Events import StepperPositionChangeEventArgs, PositionChangeEventArgs, VelocityChangeEventArgs, CurrentChangeEventArgs, AttachEventArgs, DetachEventArgs, ErrorEventArgs
from Phidgets.Devices.AdvancedServo import AdvancedServo

import datetime
import sqlite3

def AttachAdvancedServo(databasepath, serialNumber):
	def onAttachHandler(event):
		logString = "AdvancedServo Attached " + str(event.device.getSerialNum())
		DisplayAttachedDeviceInfo(event.device)

	def onDetachHandler(event):
		logString = "AdvancedServo Detached " + str(event.device.getSerialNum())
		DisplayDetachedDeviceInfo(event.device)

		event.device.closePhidget()

	def onErrorHandler(event):
		logString = "AdvancedServo Error " + str(event.device.getSerialNum()) + ", Error: " + event.description
		print(logString)

		DisplayErrorDeviceInfo(event.device)
		
	def onServerConnectHandler(event):
		logString = "AdvancedServo Server Connect " + str(event.device.getSerialNum())

	def onServerDisconnectHandler(event):
		logString = "AdvancedServo Server Disconnect " + str(event.device.getSerialNum())

	def currentChangeHandler(event):
		logString = "AdvancedServo Current Changed"

		try:
			conn = sqlite3.connect(databasepath)

			conn.execute("INSERT INTO ADVANCEDSERVO_CURRENTCHANGE VALUES(NULL, DateTime('now'), ?, ?, ?)",
					(event.device.getSerialNum(), event.index, event.current))

			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

	def positionChangeHandler(event):
		logString = "AdvancedServo Position Changed"
		#print(logString)

		try:
			conn = sqlite3.connect(databasepath)

			conn.execute("INSERT INTO ADVANCEDSERVO_POSITIONCHANGE VALUES(NULL, DateTime('now'), ?, ?, ?)",
					(event.device.getSerialNum(), event.index, event.position))

			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

	def velocityChangeHandler(event):
		logString = "AdvancedServo Velocity Changed"
		#print(logString)

		try:
			conn = sqlite3.connect(databasepath)

			conn.execute("INSERT INTO ADVANCEDSERVO_VELOCITYCHANGE VALUES(NULL, DateTime('now'), ?, ?, ?)",
					(event.device.getSerialNum(), event.index, event.velocity))

			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

	try:
		p = AdvancedServo()

		p.setOnAttachHandler(onAttachHandler)
		p.setOnDetachHandler(onDetachHandler)
		p.setOnErrorhandler(onErrorHandler)
		p.setOnServerConnectHandler(onServerConnectHandler)
		p.setOnServerDisconnectHandler(onServerDisconnectHandler)

		p.setOnCurrentChangeHandler(currentChangeHandler)
		p.setOnPositionChangeHandler(positionChangeHandler)
		p.setOnVelocityChangeHandler(velocityChangeHandler)

		p.openPhidget(serialNumber)

	except PhidgetException as e:
		print("Phidget Exception %i: %s" % (e.code, e.details))
		print("Exiting...")
		exit(1)

