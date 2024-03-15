from Phidget22.Phidget import *
from Phidget22.Devices.VoltageRatioInput import *
import time

def onVoltageRatioChange(self, voltageRatio):
	print("VoltageRatio: " + str(voltageRatio))

def main():
	voltageRatioInput0 = VoltageRatioInput()

	voltageRatioInput0.setOnVoltageRatioChangeHandler(onVoltageRatioChange)

	voltageRatioInput0.openWaitForAttachment(5000)

	try:
		input("Press Enter to Stop\n")
	except (Exception, KeyboardInterrupt):
		pass

	voltageRatioInput0.close()

main()
