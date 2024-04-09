import serial
import struct
import time
import numpy
import threading

# Serial communication setup
#ser = serial.Serial('/dev/serial0', 9600, timeout=1)  # Adjust port and baud rate as needed
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

while 1:
    send_header()
    send_data(1.0,2.,3.,4.)
    time.sleep(1)
