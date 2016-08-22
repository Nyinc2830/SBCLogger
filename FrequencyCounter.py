
from DeviceInfo import DisplayAttachedDeviceInfo
from DeviceInfo import DisplayDetachedDeviceInfo
from DeviceInfo import DisplayErrorDeviceInfo

from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AccelerationChangeEventArgs, AttachEventArgs, DetachEventArgs, ErrorEventArgs
from Phidgets.Devices.FrequencyCounter import FrequencyCounter

import datetime
import sqlite3

def AttachFrequencyCounter(databasepath, serialNumber):
	def onAttachHandler(event):
		logString = "FrequencyCounter Attached " + str(event.device.getSerialNum())
		#print(logString)
		DisplayAttachedDeviceInfo(event.device)

	def onDetachHandler(event):
		logString = "FrequencyCounter Detached " + str(event.device.getSerialNum())
		#print(logString)
		DisplayDetachedDeviceInfo(event.device)

		event.device.closePhidget()

	def onErrorHandler(event):
		logString = "FrequencyCounter Error " + str(event.device.getSerialNum()) + ", Error: " + event.description
		print(logString)
		DisplayErrorDeviceInfo(event)
		
	def onServerConnectHandler(event):
		logString = "FrequencyCounter Server Connect " + str(event.device.getSerialNum())
		#print(logString)

	def onServerDisconnectHandler(event):
		logString = "FrequencyCounter Server Disconnect " + str(event.device.getSerialNum())
		#print(logString)

	def frequencyCountHandler(event):
		logString = "FrequencyCounter Count " + str(event.device.getSerialNum())
		#print(logString)

		try:
			conn = sqlite3.connect(databasepath)

			conn.execute("INSERT INTO FREQUENCY_COUNT VALUES(NULL, DateTime('now'), ?, ?, ?, ?)", 
					(event.device.getSerialNum(), event.index, event.time, event.counts))

			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]
	try:
		p = FrequencyCounter()

		p.setOnAttachHandler(onAttachHandler)
		p.setOnDetachHandler(onDetachHandler)
		p.setOnErrorhandler(onErrorHandler)
		p.setOnServerConnectHandler(onServerConnectHandler)
		p.setOnServerDisconnectHandler(onServerDisconnectHandler)

		p.setOnFrequencyCountHandler(frequencyCountHandler)

		p.openPhidget(serialNumber)

	except PhidgetException as e:
		print("Phidget Exception %i: %s" % (e.code, e.details))
		print("Exiting...")
		exit(1)

