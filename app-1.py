import serial
import sys
import time
import tkinter as tk
from tkinter import *
from tkinter.font import Font

port = "/dev/ttyS0" #USB0 on pi
rate = 9600
ser = serial.Serial(port, rate)
ser.flushInput()

class StevensBajaSAE(tk.Frame):
	"""This is the class for the application window, the app being the tkinter setup"""
	def refresh(self):
		#refresh the data input
		#input_data = ser.readline()
		#print(input_data)
		#necessary_variables:
		current_time = time.time()
		#configure all of the new data input:
		self.total_time.config(text='{:07.3f}'.format(current_time - self.initial_time))
		self.lap_time.config(text='{:07.3f}'.format(current_time - self.initial_time + 5))
		self.previous_lap_time.config(text='{:07.3f}'.format(current_time - self.initial_time + 10))

		#refresh data:
		self.master.after(5, self.refresh)

	def __init__(self, master):
		#initialize the app - the size, title, etc.
		self.master = master
		#self.frame = tk.Frame(self.master)
		self.master.title("Baja SAE Stevens")

		#Styling
		#background color
		time_background = "#%02x%02x%02x" % (128, 192, 200)
		time_label_background = "#%02x%02x%02x" % (128, 192, 200)
		#font
		time_font = Font(family="Arial", size=15)
		time_label_font = Font(family="Arial", size=10)

		#vars for widgets:
		self.initial_time = time.time()

		#create the widgets:
		self.total_time = Label(master, font = time_font, bg=time_background)
		self.total_time_label = Label(master, font = time_label_font, bg=time_label_background, text = "Total Time Elapsed")
		self.lap_time = Label(master, font = time_font, bg=time_background)
		self.lap_time_label = Label(master, font = time_label_font, bg=time_label_background, text = "Current Lap Time")
		self.previous_lap_time = Label(master, font = time_font, bg=time_background)
		self.previous_lap_time_label = Label(master, font = time_label_font, bg=time_label_background, text = "Previous Lap Time")

		#place the widgets
		self.total_time_label.grid(row=0, column=0, sticky=N+S+E+W)
		self.total_time.grid(row=1, column=0, sticky=N+S+E+W)
		self.lap_time_label.grid(row=0, column=1, sticky=N+S+E+W)
		self.lap_time.grid(row=1, column=1, sticky=N+S+E+W)
		self.previous_lap_time_label.grid(row=0, column=2, sticky=N+S+E+W)
		self.previous_lap_time.grid(row=1, column=2, sticky=N+S+E+W)

		#allow for self resizing:
		for x in range(Grid.grid_size(master)[0]):
			Grid.columnconfigure(master, x, weight=1)
		for y in range(Grid.grid_size(master)[1]):
			Grid.rowconfigure(master, y, weight=1)

		self.refresh()

def main():
	root = tk.Tk()
	app = StevensBajaSAE(root)
	root.mainloop()

if __name__ == "__main__":
	main()