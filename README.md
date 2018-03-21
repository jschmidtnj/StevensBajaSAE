# Stevens Baja SAE Dashboard 2018

## Overview

This year the Stevens Baja SAE team decided to do something different with the analog and digital data streams in the car. Instead of relying on off-the-shelf gagues, tachometers and data collection technologies, the team decided to build a custom system from the ground up, incorporating open-source technologies to make the system completely customizable. At its core, the dash systems consists of a Raspberry Pi and Arduino Nano microcontroller, with sensors to gather data throughout the car. The data is then transmitted to a remote database, where it is analyzed and produces graphed results.

## The Raspberry Pi

We are using a raspbery pi model 3 b with wifi as the main data-collector and storage system for the Dash. We chose this model because it will allow for easy interfacing with the Arduino, and has many available periferals. A 7-inch touchscreen, 2 LCDs, 3 seven-segment displays, and various button inputs are all connected to the raspberry pi for easy input and output. The GPIO pins and dedicated touch-screen-controller, in addition to built-in wifi, are all features that made the raspberry pi the best option. The pi is running Raspbian linux, an offshoot of Debian.

## The Arduino Nano

Arduinos allow for extremely fast analog and digital input and processing, in comparison to an ARM-based computer like the pi. Due to this high data input rate, and its diminutive size, the Nano was chosen to interface with all of the various sensors throughout the car. The sensors include two thermocouples for measuring temperature near the motor, two magnometers that act as tachometers for measuring RPM and speed of the car, and a GPS module for precise location data. This sensor data is preliminarily processed on the Nano, and then transferred via serial (mini usb at 9600 baud) to the raspberry pi.

## The Screen

The 7-inch touchscreen is directly interfaced with the raspberry pi. The data on the screen mimicks the data displayed on the various other screens in the dash. But the main reason for having the screen setup is to allow for variable outputs and graphics. As more sensors are added to the car, the screen can display this new data, and all that is needed is a GUI update. The GUI is programmed in python through tkinter. Actually, the whole system, excluding the arduino code, is built on this single python script, which allows for extremely easy deployment and maintenance. The tkinter program takes the data inputted from the arduino, proceses it, and then displays it in an intuitive way on the screen. Graphics are simple, but work consistently. Then, the datapoints are sent to a local mysql database on the raspberry pi.

## The Database

On the pi, a mysql database stores all of the inputted data. This database can easily be exported to a csv file, which is compatible with programs like excel, and then stored on a usb flash drive. Additionally, the database is cloned on an Amazon ec2 instance (essentially a cloud computer) so when the pi is connected to wifi, the newly-inputted data to the mysql database is automatically uploaded to the ec2 instance. This seamless communication allows for the database to have a number of unique analytics possibilities, including real-time data-updates.

## The Remote Server

The Amazon ec2 instance contains a copy of the mysql database found on the pi. It also contains a node.js server with an angularjs frontend and expressjs backend, to enable fast javascript graphs and analytics. The amazon instance has an automatic DNS, meaning a specific URL is all you need to view the inner workings and analytics of the car.

## Comclusion

Through using this new dash system, the Stevens Baja SAE team is able to provide real-time analysis of any problems in the car, as well as valuable data to show what the driver could do better when training. Data is stored redundantly, and everything about the system, from the analog output in the dash to the node.js-based website, can be fully customized. We believe this system will give the Stevens team the edge it needs to compete well this racing season.

### Notes for Deployment

git --config user.name "yourgithubusername"
git --config user.email "yourgithubemail"
git clone "http://github.com/jschmidtnj/StevensBajaSAE/"
git add -A
git commit -m "your commit message"
git push origin master
https://github.com/adafruit/Adafruit_Python_CharLCD
https://github.com/adafruit/Adafruit_Python_LED_Backpack
make sure to install serial: sudo pip3 install pyserial
run the app as python3, and all of the installs as python3
push buttons: http://razzpisampler.oreilly.com/ch07.html
pi gpio pinout: https://pinout.xyz/
