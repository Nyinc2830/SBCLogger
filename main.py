__author__ = 'James Folk'
__version__ = '0.0.1'
__date__ = 'June 15 2016'

#Basic imports
from ctypes import *
import sys
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs
from Phidgets.Phidget import Phidget
from Phidgets.Manager import Manager
from Phidgets.Phidget import PhidgetLogLevel

def accelChangeHandler(event):
	device = event.device
	index = event.index
	acceleration = event.acceleration

def temperatureChangeHandler(event):
	device = event.device
	index = event.index
	temperature = event.temperature
	potential = event.potential

def inputChangeHandler(event):
	device = event.device
	index = event.index
	value = event.value

def outputChangeHandler(event):
	device = event.device
	index = event.index
	value = event.value

def sensorChangeHandler(event):
	device = event.device
	index = event.index
	value = event.value




def managerDeviceAttached(event):
	device = event.device
	print("Manager - Device %i: %s Attached!" % (device.getSerialNum(), device.getDeviceName()))

def managerDeviceDetached(event):
	device = e.device
	print("Manager - Device %i: %s Detached!" % (device.getSerialNum(), device.getDeviceName()))

def managerErrorHandler(event):
	device = event.device
	description = event.description
	eCode = event.eCode
	print("Manager - Device %i: %s Error! (%d: %s)" % (detached.getSerialNum(), detached.getDeviceName(), eCode, description))

def managerServerConnect(event):
	device = event.device
	print("Manager - Device %i: %s Connected!" % (device.getSerialNum(), device.getDeviceName()))

def managerServerDisconnect(event):
	device = event.device
	print("Manager - Device %i: %s Disconnected!" % (device.getSerialNum(), device.getDeviceName()))


def main():
	try:
		manager = Manager()
	except RuntimeError as e:
		print("RuntimeException: %s" % e.details)
		print("Exiting...")
		exit(1)

	try:
		manager.setOnAttachHandler(managerDeviceAttached)
		manager.setOnDetachHandler(managerDeviceDetached)
		manager.setOnErrorHandler(managerErrorHandler)
		manager.setOnServerConnectHandler(managerServerConnect)
		manager.setOnServerDisconnectHandler(managerServerDisconnect)
		manager.openManager()

	except PhidgetException as e:
		print("Phidget Exception %i: %s" % (e.code, e.details))
		print("Exiting...")
		exit(1)
	try:
		manager.openManager()
	except PhidgetException as e:
		print("Phidget Exception %i: %s" % (e.code, e.details))
		print("Exiting...")
		exit(1)

	print("Press Enter to quit...")
	chr = sys.stdin.read(1)
	print("Closing...")

	try:
		manager.closeManager()
	except PhidgetException as e:
		print("Phidget Exception %i: %s" % (e.code, e.details))
		print("Exiting...")
		exit(1)
	print("Done.")
	exit(0)


if __name__ == "__main__":
	main()
