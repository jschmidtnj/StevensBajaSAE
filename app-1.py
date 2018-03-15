import serial
import math
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

	def build_fuel_gauge(tk.Frame):
		return False

	def build_dials(self, master):
		#styling:
		num_labels = 10
		offset_ticks = 10 #px
		offset_text = 20 #px
		dial_spacing = (math.pi / 3) #should be less than pi / 2
		dial_radius = 150 #px
		y_percent = 30 #y0 offset from the top
		x_percent = 6 #x0 offset from the left
		min_value_speed = 0
		max_value_speed = 120
		min_value_rpm = 0
		max_value_rpm = 3000
		
		#Dials
		width = master.winfo_width()
		height = master.winfo_height()
		x0_dial1 = width * (x_percent / 100)
		y0_dial1 = height * (y_percent / 100)
		x1_dial1 = x0_dial1 + (2 * dial_radius)
		y1_dial1 = y0_dial1 + (2 * dial_radius)
		x1_dial2 = width * ((100 - x_percent) / 100)
		x0_dial2 = x1_dial2 - (2 * dial_radius)
		y0_dial2 = height * (y_percent / 100)
		y1_dial2 = y0_dial2 + (2 * dial_radius)

		#create dials 1 and 2
		master.create_oval(x0_dial1, y0_dial1, x1_dial1, y1_dial1)
		master.create_oval(x0_dial2, y0_dial2, x1_dial2, y1_dial2)

		#add the needles: (x0_dial is the diagonal top left point when making the circle)
		def create_needle(current_value, min_value, max_value, dial_spacing, x0_dial, y0_dial, dial_radius):
			#this is the angle from the zero the dial is in (radians) 
			radians_from_min = (current_value / (max_value - min_value)) * ((2 * math.pi) - (2 *  dial_spacing))
			#if less than pi / 2
			if (radians_from_min + dial_spacing) <= (math.pi / 2):
				if radians_from_min <= 0:
					delta_x = abs(math.sin(dial_spacing) * dial_radius) * -1
					delta_y = abs(math.cos(dial_spacing) * dial_radius) * 1
				else:
					phi = (math.pi / 2) - dial_spacing - radians_from_min
					delta_x = abs(math.cos(phi) * dial_radius) * -1
					delta_y = abs(math.sin(phi) * dial_radius) * 1
			#if less than pi
			elif (radians_from_min + dial_spacing) <= (math.pi):
				phi = radians_from_min + dial_spacing - (math.pi / 2)
				delta_x = abs(math.cos(phi) * dial_radius) * -1
				delta_y = abs(math.sin(phi) * dial_radius) * -1
			#if less than 3 pi / 2
			elif (radians_from_min + dial_spacing) <= (math.pi * 3 / 2):
				phi = radians_from_min + dial_spacing - math.pi
				delta_x = abs(math.sin(phi) * dial_radius) * 1
				delta_y = abs(math.cos(phi) * dial_radius) * -1
			#if less than the max point
			else:
				if (radians_from_min + dial_spacing) >= ((2 * math.pi) - dial_spacing):
					delta_x = abs(math.sin(dial_spacing) * dial_radius) * 1
					delta_y = abs(math.cos(dial_spacing) * dial_radius) * 1
				else:
					phi = radians_from_min + dial_spacing - (math.pi * 3 / 2)
					delta_x = abs(math.cos(phi) * dial_radius) * 1
					delta_y = abs(math.sin(phi) * dial_radius) * 1
			center_point_x = x0_dial + dial_radius
			center_point_y = y0_dial + dial_radius
			master.create_line((center_point_x + delta_x), (center_point_y + delta_y), center_point_x, center_point_y)
		#create the needle for the dials:
		#dial 1: speed:
		#dial spacing is the radians of angle between the horizontal and the first zero, make sure it is less than pi / 2
		create_needle(self.speed, min_value_speed, max_value_speed, dial_spacing, x0_dial1, y0_dial1, dial_radius)
		#dial 2: rpm
		create_needle(self.rpm, min_value_rpm, max_value_rpm, dial_spacing, x0_dial2, y0_dial2, dial_radius)

		def create_tickmarks_and_labels(min_value, max_value, dial_spacing, x0_dial, y0_dial, dial_radius, offset_ticks, offset_text):
			#this method makes the tickmarks and labels. labels are defined by the x and y offsets * some value constant * -1
			radians_between_lines = ((2 * math.pi) - (2 * dial_spacing)) / num_labels
			for i in range(num_labels + 1):
				current_tick_label = i * (max_value - min_value) / num_labels
				radians_from_min = radians_between_lines * i
				if (radians_from_min + dial_spacing) <= (math.pi / 2):
					if radians_from_min <= 0:
						delta_x_on_circle = abs(math.sin(dial_spacing) * dial_radius) * -1
						delta_y_on_circle = abs(math.cos(dial_spacing) * dial_radius) * 1
						delta_x_offset_ticks = abs(math.sin(dial_spacing) * (dial_radius - offset_ticks)) * -1
						delta_y_offset_ticks = abs(math.cos(dial_spacing) * (dial_radius - offset_ticks)) * 1
						delta_x_offset_text = abs(math.sin(dial_spacing) * (dial_radius + offset_text)) * -1
						delta_y_offset_text = abs(math.cos(dial_spacing) * (dial_radius + offset_text)) * 1
					else:
						phi = (math.pi / 2) - dial_spacing - radians_from_min
						delta_x_on_circle = abs(math.cos(phi) * dial_radius) * -1
						delta_y_on_circle = abs(math.sin(phi) * dial_radius) * 1
						delta_x_offset_ticks = abs(math.cos(phi) * (dial_radius - offset_ticks)) * -1
						delta_y_offset_ticks = abs(math.sin(phi) * (dial_radius - offset_ticks)) * 1
						delta_x_offset_text = abs(math.cos(phi) * (dial_radius + offset_text)) * -1
						delta_y_offset_text = abs(math.sin(phi) * (dial_radius + offset_text)) * 1
				#if less than pi
				elif (radians_from_min + dial_spacing) <= (math.pi):
					phi = radians_from_min + dial_spacing - (math.pi / 2)
					delta_x_on_circle = abs(math.cos(phi) * dial_radius) * -1
					delta_y_on_circle = abs(math.sin(phi) * dial_radius) * -1
					delta_x_offset_ticks = abs(math.cos(phi) * (dial_radius - offset_ticks)) * -1
					delta_y_offset_ticks = abs(math.sin(phi) * (dial_radius - offset_ticks)) * -1
					delta_x_offset_text = abs(math.cos(phi) * (dial_radius + offset_text)) * -1
					delta_y_offset_text = abs(math.sin(phi) * (dial_radius + offset_text)) * -1
				#if less than 3 pi / 2
				elif (radians_from_min + dial_spacing) <= (math.pi * 3 / 2):
					phi = radians_from_min + dial_spacing - math.pi
					delta_x_on_circle = abs(math.sin(phi) * dial_radius) * 1
					delta_y_on_circle = abs(math.cos(phi) * dial_radius) * -1
					delta_x_offset_ticks = abs(math.sin(phi) * (dial_radius - offset_ticks)) * 1
					delta_y_offset_ticks = abs(math.cos(phi) * (dial_radius - offset_ticks)) * -1
					delta_x_offset_text = abs(math.sin(phi) * (dial_radius + offset_text)) * 1
					delta_y_offset_text = abs(math.cos(phi) * (dial_radius + offset_text)) * -1
				#if less than the max point
				else:
					if (radians_from_min + dial_spacing) >= ((2 * math.pi) - dial_spacing):
						delta_x_on_circle = abs(math.sin(dial_spacing) * dial_radius) * 1
						delta_y_on_circle = abs(math.cos(dial_spacing) * dial_radius) * 1
						delta_x_offset_ticks = abs(math.sin(dial_spacing) * (dial_radius - offset_ticks)) * 1
						delta_y_offset_ticks = abs(math.cos(dial_spacing) * (dial_radius - offset_ticks)) * 1
						delta_x_offset_text = abs(math.sin(dial_spacing) * (dial_radius + offset_text)) * 1
						delta_y_offset_text = abs(math.cos(dial_spacing) * (dial_radius + offset_text)) * 1
					else:
						phi = radians_from_min + dial_spacing - (math.pi * 3 / 2)
						delta_x_on_circle = abs(math.cos(phi) * dial_radius) * 1
						delta_y_on_circle = abs(math.sin(phi) * dial_radius) * 1
						delta_x_offset_ticks = abs(math.cos(phi) * (dial_radius - offset_ticks)) * 1
						delta_y_offset_ticks = abs(math.sin(phi) * (dial_radius - offset_ticks)) * 1
						delta_x_offset_text = abs(math.cos(phi) * (dial_radius + offset_text)) * 1
						delta_y_offset_text = abs(math.sin(phi) * (dial_radius + offset_text)) * 1

				center_point_x = x0_dial + dial_radius
				center_point_y = y0_dial + dial_radius
				#create the tick marks
				master.create_line((center_point_x + delta_x_on_circle), (center_point_y + delta_y_on_circle), (center_point_x + delta_x_offset_ticks), (center_point_y + delta_y_offset_ticks))
				#create the text
				master.create_text((center_point_x + delta_x_offset_text), (center_point_y + delta_y_offset_text), text=("{0:.0f}".format(current_tick_label)))

		#create tickmarks and labels for dial
		#speed
		create_tickmarks_and_labels(min_value_speed, max_value_speed, dial_spacing, x0_dial1, y0_dial1, dial_radius, offset_ticks, offset_text)
		#rpm
		create_tickmarks_and_labels(min_value_rpm, max_value_rpm, dial_spacing, x0_dial2, y0_dial2, dial_radius, offset_ticks, offset_text)


	def new_lap(self, master):
		if self.first_new_lap_click == True:
			self.first_new_lap_click = False
			self.new_lap_button.config(text="New Lap")
			#get current time
			self.initial_time = time.time()
		self.previous_laps.append(self.current_lap)
		self.current_lap = 0
		self.sum_previous_laps = sum(self.previous_laps)

	def refresh(self):
		#refresh the data input
		#input_data = ser.readline()
		#print(input_data)
		#if there are previous laps:
		if self.previous_laps != []:
			current_time = time.time() - self.initial_time
			self.current_lap = current_time - self.sum_previous_laps
			self.previous_lap_time.config(text='{:07.3f}'.format(self.previous_laps[len(self.previous_laps) - 1]))
			#there are previous laps
			self.total_time.config(text='{:07.3f}'.format(current_time))
			self.lap_time.config(text='{:07.3f}'.format(self.current_lap))
		#if there are no previous laps:
		else:
			self.previous_lap_time.config(text='n/a')

		#configure all of the new data input:
		self.speed = 50 #for speedometer
		self.rpm = 1800 #for rpm dial
		#build the dials:
		(self.master).delete("all")
		self.build_dials(self.master)
		#refresh data:
		self.master.after(10, self.refresh)

	def __init__(self, master):
		#initialize the app - the size, title, etc.
		self.master = master

		#Styling
		#Header
		#background color
		header_background = "#%02x%02x%02x" % (128, 192, 200)
		#font
		header_font = Font(family="Arial", size=15)
		#Time
		#background color
		time_background = "#%02x%02x%02x" % (128, 192, 200)
		time_label_background = "#%02x%02x%02x" % (128, 192, 200)
		#font
		time_font = Font(family="Arial", size=15)
		time_label_font = Font(family="Arial", size=10)
		#Diagnostic
		#background color
		diagnostic_background = "#%02x%02x%02x" % (128, 192, 200)
		#font
		diagnostic_font = Font(family="Arial", size=15)


		#vars for widgets:
		self.lap_count = 0
		self.previous_laps = list()
		self.current_lap = 0
		self.sum_previous_laps = 0
		self.first_new_lap_click = True

		#create the widgets:
		#time widgets
		self.total_time = Label(master, font = time_font, bg=time_background, text = "n/a")
		self.total_time_label = Label(master, font = time_label_font, bg=time_label_background, text = "Total Time Elapsed")
		self.lap_time = Label(master, font = time_font, bg=time_background, text = "n/a")
		self.lap_time_label = Label(master, font = time_label_font, bg=time_label_background, text = "Current Lap Time")
		self.previous_lap_time = Label(master, font = time_font, bg=time_background)
		self.previous_lap_time_label = Label(master, font = time_label_font, bg=time_label_background, text = "Previous Lap Time")
		#lap widget
		self.new_lap_label = Label(master, font = time_label_font, bg=time_label_background, text = "New Lap")
		self.new_lap_button = tk.Button(master, text="Start", font = time_font, bg = time_label_background)
		#when button is pressed go to the new_lap function
		self.new_lap_button.bind('<ButtonPress>', self.new_lap)
		self.lap_count = Label(master, font = time_label_font, bg=time_label_background)


		#Temperature and other diagnostic data
		self.diagnostic_header = Label(master, font = header_font, bg=header_background, text = "Diagnostic Data")
		self.engine_temp = Label(master, font = diagnostic_font, bg=diagnostic_background)

		#place the widgets
		self.total_time_label.grid(row=0, column=0, sticky=N+S+E+W)
		self.total_time.grid(row=1, column=0, sticky=N+S+E+W)
		self.lap_time_label.grid(row=0, column=1, sticky=N+S+E+W)
		self.lap_time.grid(row=1, column=1, sticky=N+S+E+W)
		self.new_lap_label.grid(row=0, column=2, sticky=N+S+E+W)
		self.new_lap_button.grid(row=1, column = 2, sticky=N+S+E+W)
		self.previous_lap_time_label.grid(row=0, column=3, sticky=N+S+E+W)
		self.previous_lap_time.grid(row=1, column=3, sticky=N+S+E+W)
		#create a space in the grid to house the canvas widgets:
		row_spacing = 6
		self.diagnostic_header.grid(row=(1 + row_spacing), column = 0, sticky=N+S+E+W)
		self.engine_temp.grid(row=(2 + row_spacing), column=0, sticky=N+S+E+W)


		#allow for self resizing:
		for x in range(Grid.grid_size(master)[0]):
			Grid.columnconfigure(master, x, weight=1)
		for y in range(Grid.grid_size(master)[1]):
			Grid.rowconfigure(master, y, weight=1)
		#refresh function
		self.refresh()


def main():
	full_screen = False
	zoom_in = False
	master = tk.Tk()
	master.title("Baja SAE Stevens")
	#default dimensions if not fullscreen: (x, y)
	master.geometry('{}x{}'.format(800, 1000))
	#enter fullscreen mode and end it
	master.attributes("-fullscreen", full_screen)
	master.attributes("-zoomed", zoom_in)
	#create the canvas
	root = Canvas(master)
	root.pack(expand=YES, fill=BOTH)
	app = StevensBajaSAE(root)
	root.mainloop()

if __name__ == "__main__":
	main()