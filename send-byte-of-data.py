import serial

port = "/dev/ttyUSB0"
ser = serial.Serial(port, 9600)
ser.flushInput()

while True:
	if ser.inWaiting() > 0:
		inputValue = ser.read(1)
		print(ord(inputValue))
