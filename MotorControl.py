
from DeviceInfo import DisplayAttachedDeviceInfo
from DeviceInfo import DisplayDetachedDeviceInfo
from DeviceInfo import DisplayErrorDeviceInfo

from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException














from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, BackEMFEventArgs, CurrentChangeEventArgs, CurrentUpdateEventArgs, InputChangeEventArgs, PositionChangeEventArgs, SensorUpdateEventArgs, VelocityChangeEventArgs

from Phidgets.Devices.MotorControl import MotorControl

import datetime
import sqlite3

def AttachMotorControl(databasepath, serialNumber):
	def onAttachHandler(event):
		logString = "MotorControl Attached " + str(event.device.getSerialNum())
		#print(logString)
		DisplayAttachedDeviceInfo(event.device)

	def onDetachHandler(event):
		logString = "MotorControl Detached " + str(event.device.getSerialNum())
		#print(logString)
		DisplayDetachedDeviceInfo(event.device)

		event.device.closePhidget()

	def onErrorHandler(event):
		logString = "MotorControl Error " + str(event.device.getSerialNum()) + ", Error: " + event.description
		print(logString)
		DisplayErrorDeviceInfo(event.device)
		
	def onServerConnectHandler(event):
		logString = "MotorControl Server Connect " + str(event.device.getSerialNum())
		#print(logString)

	def onServerDisconnectHandler(event):
		logString = "MotorControl Server Disconnect " + str(event.device.getSerialNum())
		#print(logString)

	def backEMFUpdateHandler(event):
		logString = "MotorControl BackEMF Update"
		#print(logString)

		try:
			conn = sqlite3.connect(databasepath)

			#conn.execute("INSERT INTO MOTORCONTROL_BACKEMFUPDATE VALUES(NULL, DateTime('now'), ?, ?, ?)",
					#(event.device.getSerialNum(), event.index, event.voltage))

			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

	def currentChangeHandler(event):
		logString = "MotorControl Current Change"
		#print(logString)

		try:
			conn = sqlite3.connect(databasepath)

			#conn.execute("INSERT INTO MOTORCONTROL_CURRENTCHANGE VALUES(NULL, DateTime('now'), ?, ?, ?)",
					#(event.device.getSerialNum(), event.index, event.current))

			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

	def currentUpdateHandler(event):
		logString = "MotorControl Current Update"
		#print(logString)

		try:
			conn = sqlite3.connect(databasepath)

			#conn.execute("INSERT INTO MOTORCONTROL_CURRENTUPDATE VALUES(NULL, DateTime('now'), ?, ?, ?)",
					#(event.device.getSerialNum(), event.index, event.current))

			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

	def inputChangeHandler(event):
		logString = "MotorControl Input Change"
		#print(logString)

		try:
			conn = sqlite3.connect(databasepath)

			#conn.execute("INSERT INTO MOTORCONTROL_INPUTCHANGE VALUES(NULL, DateTime('now'), ?, ?, ?)",
					#(event.device.getSerialNum(), event.index, event.state))

			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

	def positionChangeHandler(event):
		logString = "MotorControl Position Change"
		#print(logString)

		try:
			conn = sqlite3.connect(databasepath)

			#conn.execute("INSERT INTO MOTORCONTROL_POSITIONCHANGE VALUES(NULL, DateTime('now'), ?, ?, ?)",
					#(event.device.getSerialNum(), event.index, event.current))

			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

	def positionUpdateHandler(event):
		logString = "MotorControl Position Update"
		#print(logString)

		try:
			conn = sqlite3.connect(databasepath)

			#conn.execute("INSERT INTO MOTORCONTROL_POSITIONUPDATE VALUES(NULL, DateTime('now'), ?, ?, ?)",
					#(event.device.getSerialNum(), event.index, event.position))

			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

	def sensorUpdateHandler(event):
		logString = "MotorControl Sensor Update"
		#print(logString)

		try:
			conn = sqlite3.connect(databasepath)

			#conn.execute("INSERT INTO MOTORCONTROL_SENSORUPDATE VALUES(NULL, DateTime('now'), ?, ?, ?)",
					#(event.device.getSerialNum(), event.index, event.value))

			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

	def velocityChangeHandler(event):
		logString = "MotorControl Velocity Change"
		#print(logString)

		try:
			conn = sqlite3.connect(databasepath)

			conn.execute("INSERT INTO MOTORCONTROL_VELOCITYCHANGE VALUES(NULL, DateTime('now'), ?, ?, ?)",
					(event.device.getSerialNum(), event.index, event.velocity))

			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

	try:
		p = MotorControl()

		p.setOnAttachHandler(onAttachHandler)
		p.setOnDetachHandler(onDetachHandler)
		p.setOnErrorhandler(onErrorHandler)
		p.setOnServerConnectHandler(onServerConnectHandler)
		p.setOnServerDisconnectHandler(onServerDisconnectHandler)

		p.setOnBackEMFUpdateHandler (backEMFUpdateHandler)
		p.setOnCurrentChangeHandler (currentChangeHandler)
		p.setOnCurrentUpdateHandler (currentUpdateHandler)
		p.setOnInputChangeHandler   (inputChangeHandler)
		p.setOnPositionChangeHandler(positionChangeHandler)
		p.setOnPositionUpdateHandler(positionUpdateHandler)
		p.setOnSensorUpdateHandler  (sensorUpdateHandler)
		p.setOnVelocityChangeHandler(velocityChangeHandler)

		p.openPhidget(serialNumber)

	except PhidgetException as e:
		print("Phidget Exception %i: %s" % (e.code, e.details))
		print("Exiting...")
		exit(1)

