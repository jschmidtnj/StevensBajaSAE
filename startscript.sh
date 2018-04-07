#!/bin/sh
#OCCURS ON STARTUP OF PI

xinput --set-prop 'FT5406 memory based driver' 'Coordinate Transformation Matrix' 0 1 0 -1 0 1 0 0 1
sudo su
brightness=30
echo $brightness > /sys/class/backlight/rpi_backlight/brightness
exit
cd /home/pi/Desktop/StevensBajaSAE
git pull origin master
git add -A
git commit -m "added data files"
git push origin master
python3 /home/pi/Desktop/StevensBajaSAE/app-1.py