#!/bin/sh
#OCCURS ON STARTUP OF PI

cd /home/pi/Desktop/StevensBajaSAE
git pull origin master
sudo mount /dev/sda1 /mnt/usb/
python3 /home/pi/Desktop/StevensBajaSAE/app-1.py