from Phidget22.Phidget import *
from Phidget22.Devices.VoltageRatioInput import *
import time

'''
UART communicate of F28379D and raspberry pi through python
ref: https://pyserial.readthedocs.io/en/latest/shortintro.html
Yixiao Liu 11/15/2022

ttyAMA1 has gpio0(pin27) as TX and gpio1(pin28) as RX
connected with SCID of F28(pin 9 RX, pin 10 TX)
run F28 code first
'''
import serial
import struct
from serial import Serial

# '''
# 1) Send "**" as header from pi to F28 and receive 10 floats F28 sends back
# '''
# # write header for F28 to send 10 floats
# ser.write(str.encode('*')) 
# ser.write(str.encode('*'))

# # wait for 40 bytes(10 floats)
# s = ser.read(40) # read 40 bytes
# floats = struct.unpack('ffffffffff',s) # unpack 40 bytes as 10 floats
# print(floats)

#def serialSend(self, data):
    '''
    2) Send "##" as header, then follow by 10 floats to F28
    '''
    # ser.write(str.encode('#')) 
    # ser.write(str.encode('#'))
    # ser.write(struct.pack('f',data))

#Insert your gain value from the Phidget Control Panel
gain = [2e8,2e8,2e8,2e8]

#The offset is calculated in tareScale
offset = [0,0,0,0]

calibrated = [False,False,False,False]

#Calculate offset
def tareScale(ch):    
    global offset, calibrated
    num_samples = 4

    for i in range(num_samples):
        offset[ch.getChannel()] += ch.getVoltageRatio()
        time.sleep(ch.getDataInterval()/1000.0)
        
    offset /= num_samples
    calibrated = True    


#Declare any event handlers here. These will be called every time the associated event occurs.

def onVoltageRatioChange(self, voltageRatio):
	print("VoltageRatio [" + str(self.getChannel()) + "]: " + str(voltageRatio))
	
	if(calibrated):
    #Apply the calibration parameters (gain, offset) to the raw voltage ratio
	#If there is a preload, add it to offset like this (voltageRatio - offset[self.getChannel()+preload])
        weight = (voltageRatio - offset[self.getChannel()]) * gain[self.getChannel()]
        print("Weight [" + str(self.getChannel()) + "]: " + str(weight))
		ser.write(str.encode('#')) 
		ser.write(str.encode('#'))
		ser.write(struct.pack('f',weight))

def main():
	#Create your Phidget channels
	voltageRatioInput0 = VoltageRatioInput()
	voltageRatioInput1 = VoltageRatioInput()
	voltageRatioInput2 = VoltageRatioInput()
	voltageRatioInput3 = VoltageRatioInput()

	#Set addressing parameters to specify which channel to open (if any)
	voltageRatioInput0.setChannel(0)
	voltageRatioInput1.setChannel(1)
	voltageRatioInput2.setChannel(2)
	voltageRatioInput3.setChannel(3)

	#Assign any event handlers you need before calling open so that no events are missed.
	voltageRatioInput0.setOnVoltageRatioChangeHandler(onVoltageRatioChange)
	voltageRatioInput1.setOnVoltageRatioChangeHandler(onVoltageRatioChange)
	voltageRatioInput2.setOnVoltageRatioChangeHandler(onVoltageRatioChange)
	voltageRatioInput3.setOnVoltageRatioChangeHandler(onVoltageRatioChange)

	#Open your Phidgets and wait for attachment
	voltageRatioInput0.openWaitForAttachment(5000)
	voltageRatioInput1.openWaitForAttachment(5000)
	voltageRatioInput2.openWaitForAttachment(5000)
	voltageRatioInput3.openWaitForAttachment(5000)

	#Do stuff with your Phidgets here or in your event handlers.

	try:
		input("Press Enter to Stop\n")
	except (Exception, KeyboardInterrupt):
		pass

	#Close your Phidgets once the program is done.
	voltageRatioInput0.close()
	voltageRatioInput1.close()
	voltageRatioInput2.close()
	voltageRatioInput3.close()

main()
