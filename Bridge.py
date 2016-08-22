
from DeviceInfo import DisplayAttachedDeviceInfo
from DeviceInfo import DisplayDetachedDeviceInfo
from DeviceInfo import DisplayErrorDeviceInfo

from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, BridgeDataEventArgs
from Phidgets.Devices.Bridge import Bridge

import datetime
import sqlite3

def AttachBridge(databasepath, serialNumber):
	def onAttachHandler(event):
		logString = "Bridge Attached " + str(event.device.getSerialNum())
		#print(logString)
		DisplayAttachedDeviceInfo(event.device)

	def onDetachHandler(event):
		logString = "Bridge Detached " + str(event.device.getSerialNum())
		#print(logString)
		DisplayDetachedDeviceInfo(event.device)

		event.device.closePhidget()

	def onErrorHandler(event):
		logString = "Bridge Error " + str(event.device.getSerialNum()) + ", Error: " + event.description
		print(logString)

		DisplayErrorDeviceInfo(event)
		
	def onServerConnectHandler(event):
		logString = "Bridge Server Connect " + str(event.device.getSerialNum())
		#print(logString)

	def onServerDisconnectHandler(event):
		logString = "Bridge Server Disconnect " + str(event.device.getSerialNum())
		#print(logString)

	def bridgeDataHandler(event):
		logString = "Bridge Data " + str(event.device.getSerialNum())
		#print(logString)

		try:
			conn = sqlite3.connect(databasepath)

			conn.execute("INSERT INTO BRIDGE_DATA VALUES(NULL, DateTime('now'), ?, ?, ?)", 
					(event.device.getSerialNum(), event.index, event.value))

			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]
	try:
		p = Bridge()

		p.setOnAttachHandler(onAttachHandler)
		p.setOnDetachHandler(onDetachHandler)
		p.setOnErrorhandler(onErrorHandler)
		p.setOnServerConnectHandler(onServerConnectHandler)
		p.setOnServerDisconnectHandler(onServerDisconnectHandler)

		p.setOnBridgeDataHandler(bridgeDataHandler)

		p.openPhidget(serialNumber)

	except PhidgetException as e:
		print("Phidget Exception %i: %s" % (e.code, e.details))
		print("Exiting...")
		exit(1)

