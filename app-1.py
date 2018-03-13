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

	def new_lap(self, master):
		self.previous_laps.append(self.current_lap)
		self.current_lap = 0
		self.sum_previous_laps = sum(self.previous_laps)

	def refresh(self):
		#refresh the data input
		#input_data = ser.readline()
		#print(input_data)
		#necessary_variables:
		current_time = time.time() - self.initial_time
		#if there are previous laps:
		if self.previous_laps != []:
			self.current_lap = current_time - self.sum_previous_laps
			self.previous_lap_time.config(text='{:07.3f}'.format(self.previous_laps[len(self.previous_laps) - 1]))
		#if there are no previous laps:
		else:
			self.current_lap = current_time
			self.previous_lap_time.config(text='n/a')

		self.total_time.config(text='{:07.3f}'.format(current_time))
		self.lap_time.config(text='{:07.3f}'.format(self.current_lap))

		#configure all of the new data input:

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
		self.lap_count = 0
		self.previous_laps = list()
		self.current_lap = 0
		self.sum_previous_laps = 0

		#create the widgets:
		#time widgets
		self.total_time = Label(master, font = time_font, bg=time_background)
		self.total_time_label = Label(master, font = time_label_font, bg=time_label_background, text = "Total Time Elapsed")
		self.lap_time = Label(master, font = time_font, bg=time_background)
		self.lap_time_label = Label(master, font = time_label_font, bg=time_label_background, text = "Current Lap Time")
		self.previous_lap_time = Label(master, font = time_font, bg=time_background)
		self.previous_lap_time_label = Label(master, font = time_label_font, bg=time_label_background, text = "Previous Lap Time")
		#lap widget
		self.new_lap_label = Label(master, font = time_label_font, bg=time_label_background, text = "New Lap")
		self.new_lap_button = tk.Button(master, text="Click Here", font = time_font, bg = time_label_background)
		#when button is pressed go to the new_lap function
		self.new_lap_button.bind('<ButtonPress>', self.new_lap)
		self.lap_count = Label(master, font = time_label_font, bg=time_label_background)

		#place the widgets
		self.total_time_label.grid(row=0, column=0, sticky=N+S+E+W)
		self.total_time.grid(row=1, column=0, sticky=N+S+E+W)
		self.lap_time_label.grid(row=0, column=1, sticky=N+S+E+W)
		self.lap_time.grid(row=1, column=1, sticky=N+S+E+W)
		self.new_lap_label.grid(row=0, column=2, sticky=N+S+E+W)
		self.new_lap_button.grid(row=1, column = 2, sticky=N+S+E+W)
		self.previous_lap_time_label.grid(row=0, column=3, sticky=N+S+E+W)
		self.previous_lap_time.grid(row=1, column=3, sticky=N+S+E+W)

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