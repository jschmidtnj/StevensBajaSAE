#!/bin/sh
#OCCURS ON STARTUP OF PI

cd /home/pi/Desktop/StevensBajaSAE
git pull origin master
sudo mount /dev/sda1 /mnt/usb/
cd /home/pi/Desktop/StevensBajaSAE
git pull origin master
git add -A
git commit -m "added data files"
git push origin master
python3 /home/pi/Desktop/StevensBajaSAE/app-1.py
^c^c^c
python3 /home/pi/Desktop/StevensBajaSAE/app-1.py