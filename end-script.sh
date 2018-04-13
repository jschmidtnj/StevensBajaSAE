#!/bin/sh

#use git config remote.origin.url https://jschmidtnj:PASSWORD@github.com/jschmidtnj/StevensBajaSAE.git if there are login errors
sudo mysql -u "root" < sql-to-csv.sql
sudo chmod -R 777 /tmp
sudo chmod -R 777 /mnt
cd /tmp
file_name=data.csv
current_time=$(date +"%Y-%m-%d-%H-%M-%S")
new_filename=$current_time-$file_name
mv $file_name /home/pi/Desktop/StevensBajaSAE/data/$new_filename
cat /home/pi/Desktop/StevensBajaSAE/data/$new_filename > /home/pi/Desktop/StevensBajaSAE/data/current_data_file.csv
sudo cp /home/pi/Desktop/StevensBajaSAE/data/$new_filename /mnt/usb/data
cd /home/pi/Desktop/StevensBajaSAE
git add -A
git commit -m "added data files"
git push origin master
