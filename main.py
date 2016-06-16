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
from Phidgets.Devices.InterfaceKit import InterfaceKit

def accelChangeHandler(event):
	device = event.device
	index = event.index
	acceleration = event.acceleration

def temperatureChangeHandler(event):
	device = event.device
	index = event.index
	temperature = event.temperature
	potential = event.potential





def managerDeviceAttached(event):
	device = event.device
	#print("Manager - Device %i: %s Attached!" % (device.getSerialNum(), device.getDeviceName()))
	deviceClass = device.getDeviceClass()

	if deviceClass == 2:
		#attach accelerometer
		#ACCELEROMETER = 2        - Phidgets.Accelerometer
		print("Attach Accelerometer")
	elif deviceClass == 3:
		#attach advancedservo
		#ADVANCEDSERVO = 3        - Phidgets.AdvanceServo
		print("Attach AdvanceServo")
	elif deviceClass == 22:
		#attach analog
		#ANALOG = 22              - Phidgets.Analog
		print("Attach Analog")
	elif deviceClass == 23:
		#attach bridge
		#BRIDGE = 23              - Phidgets.Bridge
		print("Attach Bridge")
	elif deviceClass == 4:
		#attach encoder
		#ENCODER = 4              - Phidgets.Encoder
		print("Attach Encoder")
	elif deviceClass == 21:
		#attach frequency counter
		#FREQUENCYCOUNTER = 21    - Phidgets.FrequencyCounter
		print("Attach FrequencyCounter")
	elif deviceClass == 5:
		#attach gps
		#GPS = 5                  - Phidgets.GPS
		print("Attach GPS")
	elif deviceClass == 7:
		#attach interface kit
		#INTERFACEKIT = 7         - Phidgets.InterfaceKit 
		print("Attach InterfaceKit")

		def inputChangeHandler(event):
			device = event.device
			index = event.index
			state = event.state
			print("IK - Index %i: State %i Input Change Handler!" % (index, state))
		def outputChangeHandler(event):
			device = event.device
			index = event.index
			state = event.state
			print("IK - Index %i: State %i Output Change Handler!" % (index, state))

		def sensorChangeHandler(event):
			device = event.device
			index = event.index
			value = event.value
			print("IK - Index %i: Value %i Sensor Change Handler!" % (index, value))
		try:
			ik = InterfaceKit()
			ik.setOnInputChangeHandler(inputChangeHandler)
			ik.setOnOutputChangeHandler(outputChangeHandler)
			ik.setOnSensorChangeHandler(sensorChangeHandler)
			ik.openPhidget(device.getSerialNum())
		except PhidgetException as e:
			print("Phidget Exception %i: %s" % (e.code, e.details))
			print("Exiting...")
			exit(1)

	elif deviceClass == 19:
		#attach ir
		#IR = 19                  - Phidgets.IR
		print("Attach IR")
	elif deviceClass == 8:
		#attach led
		#LED = 8                  - Phidgets.LED
		print("Attach LED")
	elif deviceClass == 9:
		#attach motorcontrol
		#MOTORCONTROL = 9         - Phidgets.MotorControl
		print("Attach MotorControl")
	elif deviceClass == 1:
		#attach nothing
		#NOTHING = 1
		print("Attach Nothing")
	elif deviceClass == 10:
		#attach phsensor
		#PHSENSOR = 10            - Phidgets.PHSensor
		print("Attach PHSensor")
	elif deviceClass == 11:
		#attach rfid
		#RFID = 11                - Phidgets.RFID
		print("Attach RFID")
	elif deviceClass == 12:
		#attach servo
		#SERVO = 12               - Phidgets.Servo
		print("Attach Servo")
	elif deviceClass == 20:
		#attach spatial
		#SPATIAL = 20             - Phidgets.Spatial
		print("Attach Spatial")
	elif deviceClass == 13:
		#attach stepper
		#STEPPER = 13             - Phidgets.Stepper
		print("Attach Stepper")
	elif deviceClass == 14:
		#attach temperature sensor
		#TEMPERATURESENSOR = 14   - Phidgets.TemperatureSensor
		print("Attach TemperatureSensor")
	elif deviceClass == 15:
		#attach textlcd
		#TEXTLCD = 15             - Phidgets.TextLCD
		print("Attach TextLCD")
	elif deviceClass == 16:
		#attach textled
		print("TEXTLED not supported")
	elif deviceClass == 17:
		#attach weight sensor
		print("WEIGHTSENSOR not supported")

	#TEXTLED = 16
	#WEIGHTSENSOR = 17
	

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
