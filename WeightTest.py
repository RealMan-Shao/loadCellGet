from Phidget22.Phidget import *
from Phidget22.Devices.VoltageRatioInput import *
import serial
import struct
import time
import numpy
import threading

# Serial communication setup
ser = serial.Serial(
    port="/dev/ttyTHS1",
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)

# Header and data sending functions
def send_header():
    ser.write(str.encode('#'))  # Sending "##" as the header
    ser.write(str.encode('#'))
def send_data(data1,data2,data3,data4):
    ser.write(struct.pack('f', data1))  # Pack and send the float data
    ser.write(struct.pack('f', data2))
    ser.write(struct.pack('f', data3))
    ser.write(struct.pack('f', data4))
    
def sendThread():
        while True:
        # print(weightList[1])
            send_header()  # Send header before sending data
            send_data(weightList[0],weightList[1],weightList[2],weightList[3])  # Send the calculated weight      
            time.sleep(0.1)
            
# Insert your gain value from the Phidget Control Panel
gain = [2e7, 2e7, 2e7, 2e7]

# The offset is calculated in tareScale
offset = [0, 0, 0, 0]

calibrated = [True, True, True, True]

weightList=[0,0,0,0]

# Calculate offset
def tareScale(ch):    
    global offset, calibrated
    num_samples = 4

    for i in range(num_samples):
        offset[ch.getChannel()] += ch.getVoltageRatio()
        time.sleep(ch.getDataInterval()/1000.0)
    offset[ch.getChannel()] /= num_samples
    calibrated[ch.getChannel()] = True    


# Declare any event handlers here. These will be called every time the associated event occurs.

def onVoltageRatioChange(self, voltageRatio):
    # Apply the calibration parameters (gain, offset) to the raw voltage ratio
    # If there is a preload, add it to offset like this (voltageRatio - offset[self.getChannel()+preload])
    if calibrated[self.getChannel()]:
        weightList[self.getChannel()] = ((voltageRatio - offset[self.getChannel()]) * gain[self.getChannel()])
        #print("Weight [" + str(self.getChanne(l()) + "]: " + str(weight)

def main():    
    # Create your Phidget channels
    voltageRatioInput0 = VoltageRatioInput()
    voltageRatioInput1 = VoltageRatioInput()
    voltageRatioInput2 = VoltageRatioInput()
    voltageRatioInput3 = VoltageRatioInput()

    # Set addressing parameters to specify which channel to open (if any)
    voltageRatioInput0.setChannel(0)
    voltageRatioInput1.setChannel(1)
    voltageRatioInput2.setChannel(2)
    voltageRatioInput3.setChannel(3)

    # Assign any event handlers you need before calling open so that no events are missed.
    voltageRatioInput0.setOnVoltageRatioChangeHandler(onVoltageRatioChange)
    voltageRatioInput1.setOnVoltageRatioChangeHandler(onVoltageRatioChange)
    voltageRatioInput2.setOnVoltageRatioChangeHandler(onVoltageRatioChange)
    voltageRatioInput3.setOnVoltageRatioChangeHandler(onVoltageRatioChange)

    # Open your Phidgets and wait for attachment
    voltageRatioInput0.openWaitForAttachment(5000)
    voltageRatioInput1.openWaitForAttachment(5000)
    voltageRatioInput2.openWaitForAttachment(5000)
    voltageRatioInput3.openWaitForAttachment(5000)

    # Do stuff with your Phidgets here or in your event handlers.
    time.sleep(1)
    voltageRatioInput0.setDataInterval(16)
    voltageRatioInput1.setDataInterval(16)
    voltageRatioInput2.setDataInterval(16)
    voltageRatioInput3.setDataInterval(16)
    #tareScale(voltageRatioInput0)
    
    send_thread = threading.Thread(target = sendThread)
    send_thread.start
    
    try:
        input("Press Enter to Stop\n")
    except (Exception, KeyboardInterrupt):
        pass
      

    # Close your Phidgets once the program is done.
    voltageRatioInput0.close()
    voltageRatioInput1.close()
    voltageRatioInput2.close()
    voltageRatioInput3.close()

main()
