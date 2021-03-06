import serial
import os
import envoy
import math
import sys
import time
from datetime import datetime
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
from Adafruit_LED_Backpack import SevenSegment
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
import peewee
from peewee import *
#peewee is for mysql stuff

#MySQL database
db = MySQLDatabase('StevensBajaSAEData', user='car', passwd='data')

#create 2 database classes
class RealTimeData(Model):
    rpm = CharField()
    speed = CharField()
    fuel_level = CharField()
    temp_1 = CharField()
    temp_2 = CharField()
    lap_distance = CharField()
    total_distance = CharField()
    driving_mode = CharField()
    previous_lap_time = CharField()
    current_lap_time = CharField()
    total_time = CharField()
    lap_count = CharField()
    current_time = CharField()
    latitude = CharField()
    longitude = CharField()
    altitude = CharField()

    class Meta:
        database = db

class PreviousLapSummary(Model):
	previous_lap_time = CharField()
	average_rpm = CharField()
	average_speed = CharField()
	total_time = CharField()
	lap_count = CharField()
	current_time = CharField()
	average_temp_1 = CharField()
	average_temp_2 = CharField()

	class Meta:
            database = db

class RaceSummary(Model):
	lap_count = CharField()
	total_time = CharField()
	average_rpm = CharField()
	average_speed = CharField()
	average_temp_1 = CharField()
	average_temp_2 = CharField()

	class Meta:
	    database = db

db.create_tables([RealTimeData, PreviousLapSummary, RaceSummary])

#setup for buttons:
GPIO.setmode(GPIO.BCM)
#pushbutton pin numbers:
button_1_pin = 20 #BCM 20
GPIO.setup(button_1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
'''
button_2_pin = 20 #BCM 20
GPIO.setup(button_2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
'''

#LCD 1:
# Raspberry Pi pin configuration:
lcd_1_rs        = 25  # Note this might need to be changed to 21 for older revision Pi's.
lcd_1_en        = 24
lcd_1_d4        = 23
lcd_1_d5        = 17
lcd_1_d6        = 18
lcd_1_d7        = 22
lcd_1_backlight = 4

# Define LCD column and row size for 16x2 LCD.
lcd_1_columns = 16
lcd_1_rows    = 2

# Initialize the LCD using the pins above.
lcd_1 = LCD.Adafruit_CharLCD(lcd_1_rs, lcd_1_en, lcd_1_d4, lcd_1_d5, lcd_1_d6, lcd_1_d7, lcd_1_columns, lcd_1_rows, lcd_1_backlight)

#LCD 2:
# Raspberry Pi pin configuration:
lcd_2_rs        = 25  # Note this might need to be changed to 21 for older revision Pi's.
lcd_2_en        = 24
lcd_2_d4        = 23
lcd_2_d5        = 17
lcd_2_d6        = 18
lcd_2_d7        = 22
lcd_2_backlight = 4

lcd_2_columns = 16
lcd_2_rows    = 2

# Initialize the LCD using the pins above.
#lcd_2 = LCD.Adafruit_CharLCD(lcd_2_rs, lcd_2_en, lcd_2_d4, lcd_2_d5, lcd_2_d6, lcd_2_d7, lcd_2_columns, lcd_2_rows, lcd_2_backlight)


port = "/dev/ttyUSB0" #ttyS0 on other
rate = 115200
ser = serial.Serial(port, rate)
ser.flushInput()


#initialize the seven-segment displays:
seven_segment_display_1 = SevenSegment.SevenSegment(address=0x70)
seven_segment_display_1.begin()
#3 seven segment displays
seven_segment_display_2 = SevenSegment.SevenSegment(address=0x71)
seven_segment_display_2.begin()
'''
seven_segment_display_3 = SevenSegment.SevenSegment(address=0x50)
seven_segment_display_3.begin()
'''

class StevensBajaSAE(tk.Frame):
	"""This is the class for the application window, the app being the tkinter setup"""
	def on_closing(self):
		if messagebox.askokcancel("Quit", "Do you want to quit?"):
			#send data to the database
			lap_count = len(self.previous_laps) + 1
			average_rpm_data = 0
			average_speed_data = 0
			average_temp_1_data = 0
			average_temp_2_data = 0
			count = 0
			for datapoint in PreviousLapSummary.select():
				average_rpm += datapoint.rpm
				average_speed_data += datapoint.speed
				average_temp_1_data += datapoint.temp_1
				average_temp_2_data += datapoint.temp_2
				count += 1
			if count != 0:
                            average_rpm_data /= count
                            average_speed_data /= count
                            average_temp_1_data /= count
                            average_temp_2_data /= count
                            race_summary_entry = RaceSummary.create(average_rpm = average_rpm_data, average_speed = average_speed_data, total_time = self.total_time, lap_count = lap_count, average_temp_1 = average_temp_1_data, average_temp_2 = average_temp_2_data)
                            race_summary_entry.save()
			#close window
			(self.master).destroy()
			#run the mysql script to csv
			my_path = os.path.dirname(os.path.abspath(__file__))
			envoy.run('./end-script.sh', cwd=my_path)
			exit()

	def build_driving_mode_indicator(self, driving_mode):
                #styling:
		main_label_font = Font(family="Arial", size=30)
		secondary_label_font = Font(family="Arial", size=12)
		offset_secondary_label = 35 #px
		y_percent = 30 #y0 offset from the top
		x_percent = 0 #x0 offset to the left of the center

		x0_main_label = (self.width * (.5 - x_percent / 100))
		y0_main_label = self.height * (y_percent / 100)

		#0 = forward, 1 = neutral, 2 = reverse
		if driving_mode == 0:
			#forward
			driving_mode_text = "F"
			secondary_label_1_text = "N"
			secondary_label_2_text = "R"
			secondary_label_1_offset_x = 1 * offset_secondary_label
			secondary_label_2_offset_x = 2 * offset_secondary_label
		elif driving_mode == 1:
			#neutral
			secondary_label_1_text = "F"
			driving_mode_text = "N"
			secondary_label_2_text = "R"
			secondary_label_1_offset_x = -1 * offset_secondary_label
			secondary_label_2_offset_x = 1 * offset_secondary_label
		else:
			#reverse
			secondary_label_1_text = "F"
			secondary_label_2_text = "N"
			driving_mode_text = "R"
			secondary_label_1_offset_x = -2 * offset_secondary_label
			secondary_label_2_offset_x = -1 * offset_secondary_label

		#create the main text:
		(self.master).create_text(x0_main_label, y0_main_label, text=driving_mode_text, font=main_label_font)
		(self.master).create_text(x0_main_label + secondary_label_1_offset_x, y0_main_label, text=secondary_label_1_text, font=secondary_label_font)
		(self.master).create_text(x0_main_label +  secondary_label_2_offset_x, y0_main_label, text=secondary_label_2_text, font=secondary_label_font)


	def build_fuel_gauge(self, fuel_level):
		#styling:
		out_of_fuel_threshold = 5 #percent
		out_of_fuel_label = "OUT OF FUEL"
		out_of_fuel_font = Font(family="Arial", size=30)
		main_label = "Fuel"
		main_label_font = Font(family="Arial", size=20)
		offset_main_label_x = 0 #px left
		offset_main_label_y = 25 #px up
		current_fuel_level_x_offset = 35 #px
		current_fuel_level_indicator_font = Font(family="Arial", size=12)
		text_label_font = Font(family="Arial", size=12)
		tick_length = 10 #px
		text_offset = 20 #px
		num_labels = 3
		background_guage_color = (192, 192, 192)
		guage_green = (53, 134, 0)
		guage_yellow = (210, 180, 1)
		guage_red = (166, 0, 7)
		num_labels = 3
		offset_text = 20 #px
		width_of_fuelguage = 300 #px
		height_of_fuelguage = 50 #px
		y_percent = 62 #y0 offset from the top
		x_percent = 0 #x0 offset to the left of the center

		#avoid potential problems:
		if fuel_level < 0:
			fuel_level = 0
		elif fuel_level > 100:
			fuel_level = 100
		
		#background_guage
		x0_background_guage = (self.width * (.5 - x_percent / 100)) - (width_of_fuelguage / 2)
		y0_background_guage = self.height * (y_percent / 100)
		x1_background_guage = (self.width * (.5 - x_percent / 100)) + (width_of_fuelguage / 2)
		y1_background_guage = (self.height * (y_percent / 100)) + height_of_fuelguage

		#indicator_guage
		x0_indicator_guage = (self.width * (.5 - x_percent / 100)) - (width_of_fuelguage / 2)
		y0_indicator_guage = self.height * (y_percent / 100)
		x1_indicator_guage = ((self.width * (.5 - x_percent / 100)) + (width_of_fuelguage / 2)) - ((1- (fuel_level / 100)) * width_of_fuelguage)
		y1_indicator_guage = (self.height * (y_percent / 100)) + height_of_fuelguage

		#Set the background colors:
		background_guage_color = "#%02x%02x%02x" % background_guage_color

		if fuel_level > 50:
			#make the guage green
			self.fuel_guage_color = "#%02x%02x%02x" % guage_green
		elif fuel_level > 25:
			#make the guage yellow
			self.fuel_guage_color = "#%02x%02x%02x" % guage_yellow
		else:
			#make the guage red
			self.fuel_guage_color = "#%02x%02x%02x" % guage_red

		#create background guage:
		(self.master).create_rectangle(x0_background_guage, y0_background_guage, x1_background_guage, y1_background_guage, fill=background_guage_color)
		#create indicator guage:
		(self.master).create_rectangle(x0_indicator_guage, y0_indicator_guage, x1_indicator_guage, y1_indicator_guage, fill=self.fuel_guage_color)

		#create the labels and tickmarks:
		spacing = (width_of_fuelguage / num_labels)
		difference_in_value = (100 / num_labels)
		for i in range(num_labels + 1):
			#current tick
			current_tick_label = difference_in_value * i
			#offset from x0 y0
			delta_x = i * spacing
			delta_y = height_of_fuelguage #ticks below the guage
			#create the ticks
			(self.master).create_line((x0_background_guage + delta_x), (y0_background_guage + delta_y), (x0_background_guage + delta_x), (y0_background_guage + delta_y + tick_length))
			#create the text
			(self.master).create_text((x0_background_guage + delta_x), (y0_background_guage + delta_y + text_offset), text=("{0:.0f}".format(current_tick_label)), font=text_label_font)

		#create the main label
		(self.master).create_text((x0_background_guage + (width_of_fuelguage / 2) - offset_main_label_x), (y0_background_guage - offset_main_label_y), text=main_label, font=main_label_font)

		#create the out of fuel label
		if fuel_level < out_of_fuel_threshold:
			(self.master).create_text((x0_background_guage + (width_of_fuelguage / 2)), (y0_background_guage + (height_of_fuelguage / 2)), text=out_of_fuel_label, font=out_of_fuel_font)
		else:
                    #create current level label
                    (self.master).create_text((x1_indicator_guage + current_fuel_level_x_offset), (y0_background_guage + (height_of_fuelguage / 2)), text=("{0:.02f}%".format(fuel_level)), font=current_fuel_level_indicator_font)


	def create_tickmarks_and_labels(self, min_value, max_value, dial_spacing, x0_dial, y0_dial, dial_radius, offset_ticks, offset_text, num_labels, text_label_font):
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
			(self.master).create_line((center_point_x + delta_x_on_circle), (center_point_y + delta_y_on_circle), (center_point_x + delta_x_offset_ticks), (center_point_y + delta_y_offset_ticks))
			#create the text
			(self.master).create_text((center_point_x + delta_x_offset_text), (center_point_y + delta_y_offset_text), text=("{0:.0f}".format(current_tick_label)), font=text_label_font)

	#add the needles: (x0_dial is the diagonal top left point when making the circle)
	def create_needle(self, current_value, min_value, max_value, dial_spacing, x0_dial, y0_dial, dial_radius, thickness, name_of_guage, font_main_label, offset_main_label_x, offset_main_label_y):
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
		(self.master).create_line((center_point_x + delta_x), (center_point_y + delta_y), center_point_x, center_point_y, width=thickness)

		#create the main label:
		(self.master).create_text((center_point_x + offset_main_label_x), (center_point_y + offset_main_label_y), text=name_of_guage, font=font_main_label)

	def build_dials(self):
		#styling:
		speed_name = "Speed"
		rpm_name = "RPM"
		main_label_font = Font(family="Arial", size=15)
		needle_thickness = 5
		text_label_font = Font(family="Arial", size=10)
		num_labels = 10
		offset_ticks = 10 #px
		offset_text = 20 #px
		offset_main_label_x = 0 #px
		offset_main_label_y = 35 #px
		dial_spacing = (math.pi / 3) #should be less than pi / 2
		dial_radius = 75 #px
		y_percent = 38 #y0 offset from the top
		x_percent = 7 #x0 offset from the left
		min_value_speed = 0
		max_value_speed = 120
		min_value_rpm = 0
		max_value_rpm = 3000
		
		#Dials
		x0_dial1 = self.width * (x_percent / 100)
		y0_dial1 = self.height * (y_percent / 100)
		x1_dial1 = x0_dial1 + (2 * dial_radius)
		y1_dial1 = y0_dial1 + (2 * dial_radius)
		x1_dial2 = self.width * ((100 - x_percent) / 100)
		x0_dial2 = x1_dial2 - (2 * dial_radius)
		y0_dial2 = self.height * (y_percent / 100)
		y1_dial2 = y0_dial2 + (2 * dial_radius)

		#create dials 1 and 2
		(self.master).create_oval(x0_dial1, y0_dial1, x1_dial1, y1_dial1)
		(self.master).create_oval(x0_dial2, y0_dial2, x1_dial2, y1_dial2)

		#create the needle for the dials:
		#dial 1: speed:
		#dial spacing is the radians of angle between the horizontal and the first zero, make sure it is less than pi / 2
		self.create_needle(self.speed, min_value_speed, max_value_speed, dial_spacing, x0_dial1, y0_dial1, dial_radius, needle_thickness, speed_name, main_label_font, offset_main_label_x, offset_main_label_y)
		#dial 2: rpm
		self.create_needle(self.rpm, min_value_rpm, max_value_rpm, dial_spacing, x0_dial2, y0_dial2, dial_radius, needle_thickness, rpm_name, main_label_font, offset_main_label_x, offset_main_label_y)

		#create tickmarks and labels for dial
		#speed
		self.create_tickmarks_and_labels(min_value_speed, max_value_speed, dial_spacing, x0_dial1, y0_dial1, dial_radius, offset_ticks, offset_text, num_labels, text_label_font)
		#rpm
		self.create_tickmarks_and_labels(min_value_rpm, max_value_rpm, dial_spacing, x0_dial2, y0_dial2, dial_radius, offset_ticks, offset_text, num_labels, text_label_font)

	def time_info(self):
		self.current_time_int = time.time() - self.initial_time
		#if there are previous laps:
		if self.previous_laps != []:
			self.current_lap = self.current_time_int - self.sum_previous_laps
			self.previous_lap_time_data = '{0:.3f}'.format(self.previous_laps[len(self.previous_laps) - 1])
			self.previous_lap_time.config(text=self.previous_lap_time_data)
			#there are previous laps
			self.total_time_data = '{0:.3f}'.format(self.current_time_int)
			self.total_time.config(text=self.total_time_data)
			self.current_lap_time_data = '{0:.3f}'.format(self.current_lap)
			self.lap_time.config(text=self.current_lap_time_data)
		#if there are no previous laps:
		else:
			self.previous_lap_time.config(text='n/a')
		#add the current time:
		the_time_and_date = str(datetime.now())
		the_time = the_time_and_date[11:]
		the_date = the_time_and_date[:10]
		self.current_time_data = '{0}'.format(the_time[:11])
		self.current_time.config(text=self.current_time_data)
		self.lap_count_data = len(self.previous_laps)
		self.lap_count.config(text='Lap {0:.0f}'.format(self.lap_count_data))

	def added_fuel(self, master):
		self.fuel_level = 100

	def reset_gui(self, master):
            #reset the lap info
            self.added_fuel(master)
            self.first_new_lap_click = True
            self.new_lap_button.config(text="Start")
            self.total_time.config(text="n/a")
            self.lap_time.config(text="n/a")
            self.current_lap = 0
            self.sum_previous_laps = 0
            #send this data to mysql db
            self.previous_laps = []
    
	def mode_toggle(self, master):
            return
        
	def new_lap(self, master):
		if self.first_new_lap_click == True:
			self.first_new_lap_click = False
			self.new_lap_button.config(text="New Lap")
			#get current time
			self.initial_time = time.time()
		lap_count = len(self.previous_laps) + 1
		average_rpm_data = 0
		average_speed_data = 0
		average_temp_1_data = 0
		average_temp_2_data = 0
		count = 0
		for datapoint in RealTimeData.select().where(RealTimeData.lap_count == lap_count):
			average_rpm += datapoint.rpm
			average_speed_data += datapoint.speed
			average_temp_1_data += datapoint.temp_1
			average_temp_2_data += datapoint.temp_2
			count += 1
		if count != 0:
                    average_rpm_data /= count
                    average_speed_data /= count
                    average_temp_1_data /= count
                    average_temp_2_data /= count
                    previous_lap_entry = PreviousLapSummary.create(previous_lap_time = self.current_lap, average_rpm = average_rpm_data, average_speed = average_speed_data, total_time = self.total_time, lap_count = lap_count, current_time = self.current_time, average_temp_1 = average_temp_1_data, average_temp_2 = average_temp_2_data)
                    previous_lap_entry.save()
		self.previous_laps.append(self.current_lap)
		self.lap_distance_data = 0
		self.current_lap = 0
		self.sum_previous_laps = sum(self.previous_laps)

	def refresh(self):
		#TIME:
		self.time_info()

		#refresh the width and height of the screen:
		self.width = (self.master).winfo_width()
		self.height = (self.master).winfo_height()
		
		#get push button input:
		self.button_1_state = not GPIO.input(button_1_pin)
		#self.button_2_state = not GPIO.input(button_2_pin)
		#etc...
		if self.button_1_state:
			print("Button 1 Pressed")
		
		#refresh the data input
		#input_data = ser.readline()
		#print(input_data)
		#configure all of the new data input:
		#NEW DATA
		self.driving_mode = 0
		data = str(ser.readline())
		#data in the form of:rpm, speed,temp_1,temp_2
		
		data_parsed = [x for x in data.split(',')] #split by comma
		print(data_parsed)
		self.rpm = float(data_parsed[1]) #for rpm dial
		self.speed = float(data_parsed[2]) #for speedometer mph
		self.temp_1 = float(data_parsed[3]) #temp for engine
		self.temp_2 = float(data_parsed[4]) #temp for engine perimeter
		self.latitude = data_parsed[5]
		self.longitude = data_parsed[6]
		self.altitude = float(data_parsed[7])

		#add data to the labels:
		self.temperature_1.config(text='{0:.2f}'.format(self.temp_1))
		self.temperature_2.config(text='{0:.2f}'.format(self.temp_2))
		#data for the displays
		#seven-segment displays:
		self.seven_segment_display_1_data = float(self.rpm)
		self.seven_segment_display_2_data = float(self.speed)
		self.seven_segment_display_3_data = 14.222
		#adjust the fuel level:
		#if start was hit
		if self.previous_laps != [] and self.rpm != 0:
			#ln function of rpm requires three constants that need to be solved for somehow
			self.fuel_level = self.fuel_level - ((.2*math.log(self.rpm) + .05) * self.refresh_time / (self.fuel_tank_size * 40))
			distance_data = float((self.speed / 3600000 * self.refresh_time * 8.65)) #delay for program time use (ms)
			self.lap_distance_data += distance_data
			self.total_distance_data += distance_data
		else:
			self.fuel_level = self.fuel_level_starting_percentage
			self.lap_distance_data = 0
			self.total_distance_data = 0
		#LCDs:
		if self.fuel_level > 50:
			self.lcd_1_data = "Full: {0:.2f}% \n".format(self.fuel_level)
		elif self.fuel_level > 25:
			self.lcd_1_data = "LOW: {0:.2f}% \n".format(self.fuel_level)
		elif self.fuel_level > 5:
			self.lcd_1_data = "Refuel! {0:.2f}%\n".format(self.fuel_level)
		else:
			self.lcd_1_data = "OUT OF FUEL   \n"
		self.num_boxes = int(self.fuel_level / 100 * lcd_1_columns)
		num_blank = lcd_1_columns - self.num_boxes
		for _ in range(self.num_boxes):
			self.lcd_1_data += ('\x00')
		for _ in range(num_blank):
			self.lcd_1_data += ('\x01')
		self.lcd_2_data = "Hello World\nLCD1..."
		
		#send distance data
		self.lap_distance.config(text='{0:.2f}'.format(self.lap_distance_data))
		self.total_distance.config(text='{0:.2f}'.format(self.total_distance_data))

		#working with Canvas - first delete everything from before:
		(self.master).delete("all")
		#build the dials:
		self.build_dials()

		#build the fuel gauge:
		self.build_fuel_gauge(self.fuel_level)

		#build the driving mode:
		self.build_driving_mode_indicator(self.driving_mode)
		
		#send data to seven segment displays
		seven_segment_display_1.clear()
		seven_segment_display_2.clear()
		'''
		seven_segment_display_3.clear()
		'''
		seven_segment_display_1.print_float(self.seven_segment_display_1_data, decimal_digits=0)
		seven_segment_display_2.print_float(self.seven_segment_display_2_data, decimal_digits=2)
		'''
		seven_segment_display_3.print_float(self.seven_segment_display_3_data, decimal_digits=2)
		'''
		seven_segment_display_1.write_display()
		seven_segment_display_2.write_display()
		
		#send data to the LCDs
		lcd_1.set_cursor(0,0)
		#lcd_2.set_cursor(0,0)
		lcd_1.message(self.lcd_1_data)
		#lcd_2.message(self.lcd_2_data)
		
		#add data to rolling array:
		self.rpm_array.append(self.rpm)
		self.speed_array.append(self.speed)
		self.temp_1_array.append(self.temp_1)
		self.temp_2_array.append(self.temp_2)
		
		if (self.current_time_int- self.database_time) > (self.database_delay):
                    self.database_time = self.current_time_int
                    #add data to database:
                    #PROBLEM WITH PASSING LABELS IN FOR DATA
                    datapoint = RealTimeData.create(rpm = (sum(self.rpm_array) / float(len(self.rpm_array))), speed = (sum(self.speed_array) / float(len(self.speed_array))), fuel_level = self.fuel_level, temp_1 = (sum(self.temp_1_array) / float(len(self.temp_1_array))), temp_2 = (sum(self.temp_2_array) / float(len(self.temp_2_array))), lap_distance = self.lap_distance_data, total_distance = self.total_distance_data, driving_mode = self.driving_mode, previous_lap_time = self.previous_lap_time_data, current_lap_time = self.current_lap_time_data, total_time = self.total_time_data, lap_count = self.lap_count_data, current_time = self.current_time_data, latitude = self.latitude, longitude = self.longitude, altitude = self.altitude)
                    datapoint.save()

		#refresh data:
		(self.master).after(self.refresh_time, self.refresh)

	def __init__(self, master):
		#initialize the app - the size, title, etc.
		self.master = master
		
		#clear the mysql tables and run bash script
		#run the mysql script to csv
		my_path = os.path.dirname(os.path.abspath(__file__))
		envoy.run('./start-script.sh', cwd=my_path)

		#Styling
		#Header
		#background color
		header_background = "#%02x%02x%02x" % (128, 192, 200)
		#font
		header_font = Font(family="Arial", size=12)
		#Time
		#background color
		time_background = "#%02x%02x%02x" % (128, 192, 200)
		#font
		time_font = Font(family="Arial", size=12)
		lap_count_font = Font(family="Arial", size=15)
		#Diagnostic
		#background color
		diagnostic_background = "#%02x%02x%02x" % (128, 192, 200)
		current_time_background = "#%02x%02x%02x" % (128, 192, 200)
		#font
		diagnostic_font = Font(family="Arial", size=12)
		current_time_font = Font(family="Arial", size=15)
		
		#other displays:
		#LCD:
		#box char set to 0 index
		lcd_1.create_char(0, [0x1f, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f])
		#blank char set to 1 index
		lcd_1.create_char(1, [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0])
		#lcd_2.create_char(0, [0x1f, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f])
		#SSD:
		seven_segment_display_1.set_colon(False)
		'''
		seven_segment_display_2.set_colon(False)
		seven_segment_display_3.set_colon(False)
                '''
		#Pushbuttons:
		self.button_1_state = False #false = off
		#self.button_2_state = False #false = off

		#global vars for functions:
		self.refresh_time = 10 #ms
		self.database_delay = 2 #seconds between each data-poiint
		self.previous_lap_time_data = ""
		self.current_lap_time_data = ""
		self.total_time_data = ""
		self.current_time_data = ""
		self.rpm_array = []
		self.speed_array = []
		self.temp_1_array = []
		self.temp_2_array = []
		self.fuel_tank_size = 10 #gallons
		self.lap_distance_data = 0
		self.total_distance_data = 0
		self.current_gear = "P"
		self.lap_count_data = 0
		self.previous_laps = list()
		self.current_lap = 0
		self.sum_previous_laps = 0
		self.first_new_lap_click = True
		self.last_fueling_time = self.current_time_int = self.initial_time = time.time()
		self.database_time = 0
		self.fuel_level_starting_percentage = 100
		self.fuel_level = self.fuel_level_starting_percentage
		self.latitude = 0
		self.longitude = 0
		self.altitude = 0

		#create the widgets:
		#time widgets
		self.total_time = Label(master, font = time_font, bg=time_background, text = "n/a")
		self.total_time_label = Label(master, font = header_font, bg=header_background, text = "Total")
		self.lap_time = Label(master, font = time_font, bg=time_background, text = "n/a")
		self.lap_time_label = Label(master, font = header_font, bg=header_background, text = "Current")
		self.previous_lap_time = Label(master, font = time_font, bg=time_background)
		self.previous_lap_time_label = Label(master, font = header_font, bg=header_background, text = "Previous")
		#lap widget
		self.lap_count = Label(master, font = lap_count_font, bg=header_background, text="0")
		self.new_lap_button = tk.Button(master, text="Start", font = time_font, bg = time_background)
		#when button is pressed go to the new_lap function
		self.new_lap_button.bind('<ButtonPress>', self.new_lap)

		#Temperature and other diagnostic data
		self.temperature_1_header = Label(master, font = header_font, bg=header_background, text = "CRS-1")
		self.temperature_1 = Label(master, font = diagnostic_font, bg=diagnostic_background)
		self.temperature_2_header = Label(master, font = header_font, bg=header_background, text = "CRS-2")
		self.temperature_2 = Label(master, font = diagnostic_font, bg=diagnostic_background)
		self.modetoggle = tk.Button(master, text = "Mode", font = diagnostic_font, bg=diagnostic_background)
		self.current_time = Label(master, font = current_time_font, bg=current_time_background)
		self.reset_button = tk.Button(master, text = "Reset", font = diagnostic_font, bg=diagnostic_background)
		#when button is pressed go to the reset_gui function
		self.reset_button.bind('<ButtonPress>', self.reset_gui)
		#adding fuel:
		self.add_fuel = tk.Button(master, text = "Add Fuel", font = diagnostic_font, bg=diagnostic_background)
		self.add_fuel.bind('<ButtonPress>', self.added_fuel)
		self.modetoggle.bind('<ButtonPress>', self.mode_toggle)
		self.lap_distance_header = Label(master, font = header_font, bg=header_background, text = "Lap")
		self.lap_distance = Label(master, font = diagnostic_font, bg=diagnostic_background)
		self.total_distance_header = Label(master, font = header_font, bg=header_background, text = "Total")
		self.total_distance = Label(master, font = diagnostic_font, bg=diagnostic_background)
		

		#place the widgets
		self.new_lap_button.grid(row=0, column = 0, sticky=N+S+E+W)
		self.current_time.grid(row=1, column=0, sticky=N+S+E+W)
		self.previous_lap_time_label.grid(row=0, column=1, sticky=N+S+E+W)
		self.previous_lap_time.grid(row=1, column=1, sticky=N+S+E+W)
		self.lap_time_label.grid(row=0, column=2, sticky=N+S+E+W)
		self.lap_time.grid(row=1, column=2, sticky=N+S+E+W)
		self.total_time_label.grid(row=0, column=3, sticky=N+S+E+W)
		self.total_time.grid(row=1, column=3, sticky=N+S+E+W)
		self.lap_count.grid(row=0, column=4, sticky=N+S+E+W)
		self.reset_button.grid(row=1, column=4, sticky=N+S+E+W)
		#create a space in the grid to house the canvas widgets:
		row_spacing = 8
		self.temperature_1_header.grid(row=(row_spacing), column=0, sticky=N+S+E+W)
		self.temperature_1.grid(row=(1 + row_spacing), column=0, sticky=N+S+E+W)
		self.temperature_2_header.grid(row=(row_spacing), column=1, sticky=N+S+E+W)
		self.temperature_2.grid(row=(1 + row_spacing), column=1, sticky=N+S+E+W)
		self.modetoggle.grid(row=(row_spacing), column=2, sticky=N+S+E+W)
		self.add_fuel.grid(row=(1 + row_spacing), column=2, sticky=N+S+E+W)
		self.lap_distance_header.grid(row=(row_spacing), column=3, sticky=N+S+E+W)
		self.lap_distance.grid(row=(1 + row_spacing), column=3, sticky=N+S+E+W)
		self.total_distance_header.grid(row=(row_spacing), column=4, sticky=N+S+E+W)
		self.total_distance.grid(row=(1 + row_spacing), column=4, sticky=N+S+E+W)

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
	master.protocol("WM_DELETE_WINDOW", app.on_closing)
	root.mainloop()

if __name__ == "__main__":
	main()
