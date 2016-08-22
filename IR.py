
from DeviceInfo import DisplayAttachedDeviceInfo
from DeviceInfo import DisplayDetachedDeviceInfo
from DeviceInfo import DisplayErrorDeviceInfo

from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import IRCodeEventArgs, IRLearnEventArgs, IRRawDataEventArgs, AttachEventArgs, DetachEventArgs, ErrorEventArgs
from Phidgets.Devices.IR import IR, IRCode, IRCodeInfo, IRCodeLength, IREncoding, IRLearnedCode

import datetime
import sqlite3

def AttachIR(databasepath, serialNumber):
	def onAttachHandler(event):
		logString = "IR Attached " + str(event.device.getSerialNum())
		#print(logString)
		DisplayAttachedDeviceInfo(event.device)

	def onDetachHandler(event):
		logString = "IR Detached " + str(event.device.getSerialNum())
		#print(logString)
		DisplayDetachedDeviceInfo(event.device)

		event.device.closePhidget()

	def onErrorHandler(event):
		logString = "IR Error " + str(event.device.getSerialNum()) + ", Error: " + event.description
		print(logString)
		DisplayErrorDeviceInfo(event)
		
	def onServerConnectHandler(event):
		logString = "IR Server Connect " + str(event.device.getSerialNum())
		#print(logString)

	def onServerDisconnectHandler(event):
		logString = "IR Server Disconnect " + str(event.device.getSerialNum())
		#print(logString)

	def IRCodeHandler(event):
		logString = "IR Code " + str(event.device.getSerialNum())
		print(logString)

		try:
			conn = sqlite3.connect(databasepath)

			conn.execute("INSERT INTO IR_CODE VALUES(NULL, DateTime('now'), ?, ?, ?)", 
					(event.device.getSerialNum(), event.code, event.repeat))

			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

	def IRLearnHandler(event):
		logString = "IR Learn " + str(event.device.getSerialNum())
		print(logString)

		try:
			conn = sqlite3.connect(databasepath)

			conn.execute("INSERT INTO IR_LEARN VALUES(NULL, DateTime('now'), ?, ?, ?)", 
					(event.device.getSerialNum(), event.code, event.codeInfo))

			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

	def IRRawDataHandler(event):
		logString = "IR Raw Data " + str(event.device.getSerialNum())
		print(logString)

		try:
			conn = sqlite3.connect(databasepath)

			conn.execute("INSERT INTO IR_RAWDATA VALUES(NULL, DateTime('now'), ?, ?)", 
					(event.device.getSerialNum(), event.rawData))

			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

	try:
		p = IR()

		p.setOnAttachHandler(onAttachHandler)
		p.setOnDetachHandler(onDetachHandler)
		p.setOnErrorhandler(onErrorHandler)
		p.setOnServerConnectHandler(onServerConnectHandler)
		p.setOnServerDisconnectHandler(onServerDisconnectHandler)

		p.setOnIRCodeHandler   (IRCodeHandler)
		p.setOnIRLearnHandler  (IRLearnHandler)
		p.setOnIRRawDataHandler(IRRawDataHandler)

		p.openPhidget(serialNumber)

	except PhidgetException as e:
		print("Phidget Exception %i: %s" % (e.code, e.details))
		print("Exiting...")
		exit(1)

