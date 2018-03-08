import serial
import sys
import time
from Tkinter import *

port = "/dev/ttyUSB0"
rate = 9600
ser = serial.Serial(port, rate)
ser.flushInput()

app = Tk()
app.title("Baja SAE Stevens")
app.geometry("400x360+400+150")
data = Label(app, font=('times', 20, 'bold'), bg='green')
data.pack(fill=BOTH, expand=1)

def refresh_data():
	input_data = ser.readline()
	print(input_data)
	data.config(text=input_data)
	data.after(5, refresh_data)

refresh_data()
app.mainloop()
