
from DeviceInfo import DisplayAttachedDeviceInfo
from DeviceInfo import DisplayDetachedDeviceInfo
from DeviceInfo import DisplayErrorDeviceInfo

from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import SpatialDataEventArgs, AttachEventArgs, DetachEventArgs, ErrorEventArgs
from Phidgets.Devices.Spatial import Spatial, SpatialEventData, TimeSpan

import datetime
import sqlite3

def AttachSpatial(databasepath, serialNumber):
	def onAttachHandler(event):
		logString = "Spatial Attached " + str(event.device.getSerialNum())
		#print(logString)
		DisplayAttachedDeviceInfo(event.device)

	def onDetachHandler(event):
		logString = "Spatial Detached " + str(event.device.getSerialNum())
		#print(logString)
		DisplayDetachedDeviceInfo(event.device)

		event.device.closePhidget()

	def onErrorHandler(event):
		logString = "Spatial Error " + str(event.device.getSerialNum()) + ", Error: " + event.description
		#print(logString)
		DisplayErrorDeviceInfo(event.device)
		
	def onServerConnectHandler(event):
		logString = "Spatial Server Connect " + str(event.device.getSerialNum())
		#print(logString)

	def onServerDisconnectHandler(event):
		logString = "Spatial Server Disconnect " + str(event.device.getSerialNum())
		#print(logString)

	def spatialDataHandler(event):
		logString = "Spatial Changed " + str(event.device.getSerialNum())
		#print(logString)

		try:
			conn = sqlite3.connect(databasepath)
				
			index = 0
			for spatialData in enumerate(event.spatialData):
				accelX = 0
				accelY = 0
				accelZ = 0
				if len(spatialData[1].Acceleration) > 0:
					accelX = spatialData[1].Acceleration[0]
					accelY = spatialData[1].Acceleration[1]
					if len(spatialData[1].Acceleration) > 2:
						accelZ = spatialData[1].Acceleration[2]

				angularX = 0
				angularY = 0
				angularZ = 0
				if len(spatialData[1].AngularRate) > 0:
					angularX = spatialData[1].AngularRate[0]
					angularY = spatialData[1].AngularRate[1]
					if len(spatialData[1].AngularRate) > 2:
						angularZ = spatialData[1].AngularRate[2]

				magneticX = 0
				magneticY = 0
				magneticZ = 0
				if len(spatialData[1].MagneticField) > 0:
					magneticX = spatialData[1].MagneticField[0]
					magneticY = spatialData[1].MagneticField[1]
					if len(spatialData[1].AngularRate) > 2:
						magneticZ = spatialData[1].MagneticField[2]

				conn.execute("INSERT INTO SPATIAL_DATACHANGE VALUES(NULL, DateTime('now'), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
						(event.device.getSerialNum(), index, accelX, accelY, accelZ, angularX, angularY, angularZ, magneticX, magneticY, magneticZ))

				index += 1

			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

	try:
		p = Spatial()

		p.setOnAttachHandler(onAttachHandler)
		p.setOnDetachHandler(onDetachHandler)
		p.setOnErrorhandler(onErrorHandler)
		p.setOnServerConnectHandler(onServerConnectHandler)
		p.setOnServerDisconnectHandler(onServerDisconnectHandler)

		p.setOnSpatialDataHandler(spatialDataHandler)
		p.openPhidget(serialNumber)

	except PhidgetException as e:
		print("Phidget Exception %i: %s" % (e.code, e.details))
		print("Exiting...")
		exit(1)

