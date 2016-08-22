
from DeviceInfo import DisplayAttachedDeviceInfo
from DeviceInfo import DisplayDetachedDeviceInfo
from DeviceInfo import DisplayErrorDeviceInfo

from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException

from Phidgets.Events.Events import StepperPositionChangeEventArgs, PositionChangeEventArgs, VelocityChangeEventArgs, CurrentChangeEventArgs, InputChangeEventArgs, AttachEventArgs, DetachEventArgs, ErrorEventArgs
from Phidgets.Devices.Stepper import Stepper

import datetime
import sqlite3

def AttachStepper(databasepath, serialNumber):
	def onAttachHandler(event):
		logString = "Stepper Attached " + str(event.device.getSerialNum())
		#print(logString)
		DisplayAttachedDeviceInfo(event.device)

	def onDetachHandler(event):
		logString = "Stepper Detached " + str(event.device.getSerialNum())
		#print(logString)
		DisplayDetachedDeviceInfo(event.device)

		event.device.closePhidget()

	def onErrorHandler(event):
		logString = "Stepper Error " + str(event.device.getSerialNum()) + ", Error: " + event.description
		#print(logString)
		DisplayErrorDeviceInfo(event.device)
		
	def onServerConnectHandler(event):
		logString = "Stepper Server Connect " + str(event.device.getSerialNum())
		#print(logString)

	def onServerDisconnectHandler(event):
		logString = "Stepper Server Disconnect " + str(event.device.getSerialNum())
		#print(logString)

	def currentChangeHandler(event):
		logString = "Stepper Current Changed"
		#print(logString)

		try:
			conn = sqlite3.connect(databasepath)

			conn.execute("INSERT INTO STEPPER_CURRENTCHANGE VALUES(NULL, DateTime('now'), ?, ?, ?)",
					(event.device.getSerialNum(), event.index, event.current))

			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

	def inputChangeHandler(event):
		logString = "Stepper Input Changed"
		#print(logString)

		try:
			conn = sqlite3.connect(databasepath)
				
			conn.execute("INSERT INTO STEPPER_INPUTCHANGE VALUES(NULL, DateTime('now'), ?, ?, ?)",
					(event.device.getSerialNum(), event.index, int(event.state)))

			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

	def positionChangeHandler(event):
		logString = "Stepper Position Changed"
		#print(logString)

		try:
			conn = sqlite3.connect(databasepath)

			conn.execute("INSERT INTO STEPPER_POSITIONCHANGE VALUES(NULL, DateTime('now'), ?, ?, ?)",
					(event.device.getSerialNum(), event.index, event.position))

			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

	def velocityChangeHandler(event):
		logString = "Stepper Velocity Changed"
		#print(logString)

		try:
			conn = sqlite3.connect(databasepath)

			conn.execute("INSERT INTO STEPPER_VELOCITYCHANGE VALUES(NULL, DateTime('now'), ?, ?, ?)",
					(event.device.getSerialNum(), event.index, event.velocity))

			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

	try:
		p = Stepper()

		p.setOnAttachHandler(onAttachHandler)
		p.setOnDetachHandler(onDetachHandler)
		p.setOnErrorhandler(onErrorHandler)
		p.setOnServerConnectHandler(onServerConnectHandler)
		p.setOnServerDisconnectHandler(onServerDisconnectHandler)

		p.setOnCurrentChangeHandler(currentChangeHandler)
		p.setOnInputChangeHandler(inputChangeHandler)
		p.setOnPositionChangeHandler(positionChangeHandler)
		p.setOnVelocityChangeHandler(velocityChangeHandler)

		p.openPhidget(serialNumber)

	except PhidgetException as e:
		print("Phidget Exception %i: %s" % (e.code, e.details))
		print("Exiting...")
		exit(1)

