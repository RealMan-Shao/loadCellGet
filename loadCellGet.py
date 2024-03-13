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

def serialSend(self, data):
    '''
    2) Send "##" as header, then follow by 10 floats to F28
    '''
    ser.write(str.encode('#')) 
    ser.write(str.encode('#'))
    ser.write(struct.pack('f',data))

#Declare any event handlers here. These will be called every time the associated event occurs.

def onVoltageRatioInput0_VoltageRatioChange(self, voltageRatio):
	print("VoltageRatio [0]: " + str(voltageRatio))
    ser.write(str.encode('#')) 
    ser.write(str.encode('#'))
    ser.write(struct.pack('f',voltageRatio))

def onVoltageRatioInput1_VoltageRatioChange(self, voltageRatio):
	print("VoltageRatio [1]: " + str(voltageRatio))
    ser.write(str.encode('#')) 
    ser.write(str.encode('#'))
    ser.write(struct.pack('f',voltageRatio))

def onVoltageRatioInput2_VoltageRatioChange(self, voltageRatio):
	print("VoltageRatio [2]: " + str(voltageRatio))
    ser.write(str.encode('#')) 
    ser.write(str.encode('#'))
    ser.write(struct.pack('f',voltageRatio))

def onVoltageRatioInput3_VoltageRatioChange(self, voltageRatio):
	print("VoltageRatio [3]: " + str(voltageRatio))
    ser.write(str.encode('#')) 
    ser.write(str.encode('#'))
    ser.write(struct.pack('f',voltageRatio))

def main():
    
	# initialize the serial port
	ser = serial.Serial("/dev/ttyAMA1", 115200) #Open port with baud rate

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

	voltageRatioInput0.setDataRate(250)
	voltageRatioInput1.setDataRate(250)
	voltageRatioInput2.setDataRate(250)
	voltageRatioInput3.setDataRate(250)
 
	voltageRatioInput0.setDataInterval(4)
	voltageRatioInput1.setDataInterval(4)
	voltageRatioInput2.setDataInterval(4)
	voltageRatioInput3.setDataInterval(4)
 
	#Assign any event handlers you need before calling open so that no events are missed.
	voltageRatioInput0.setOnVoltageRatioChangeHandler(onVoltageRatioInput0_VoltageRatioChange)
	voltageRatioInput1.setOnVoltageRatioChangeHandler(onVoltageRatioInput1_VoltageRatioChange)
	voltageRatioInput2.setOnVoltageRatioChangeHandler(onVoltageRatioInput2_VoltageRatioChange)
	voltageRatioInput3.setOnVoltageRatioChangeHandler(onVoltageRatioInput3_VoltageRatioChange)

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
