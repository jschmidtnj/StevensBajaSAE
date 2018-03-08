import serial
import time

port = "/dev/ttyUSB0"
rate = 9600
ser = serial.Serial(port, rate)
ser.flushInput()

while True:
	print(ser.readline())
