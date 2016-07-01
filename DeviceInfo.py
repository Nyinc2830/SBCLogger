
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException

def DisplayAttachedDeviceInfo(device):
	print("|------------|----------------------------------|--------------|------------|")
	print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
	print("|------------|----------------------------------|--------------|------------|")
	print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (device.isAttached(), device.getDeviceName(), device.getSerialNum(), device.getDeviceVersion()))
	print("|------------|----------------------------------|--------------|------------|")
			
def DisplayDetachedDeviceInfo(device):
	print("|------------|----------------------------------|--------------|------------|")
	print("|- Detached -|-              Type              -|- Serial No. -|-  Version -|")
	print("|------------|----------------------------------|--------------|------------|")
	print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (device.isAttached(), device.getDeviceName(), device.getSerialNum(), device.getDeviceVersion()))
	print("|------------|----------------------------------|--------------|------------|")

def DisplayErrorDeviceInfo(e):
	try:
		print("Phidget Error %i: %s" % (e.eCode, e.description))
	except PhidgetException as e:
		print("Phidget Exception %i: %s" % (e.code, e.details))
