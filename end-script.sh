#!/bin/sh

sudo mysql -u "root" < sql-to-csv.sql
cd /tmp
sudo chmod -R 777 /tmp
file_name=data.csv
current_time=$(date +"%Y-%m-%d-%H-%M-%S")
new_filename=$current_time-$file_name
mv $file_name /home/pi/Desktop/StevensBajaSAE/data/$new_filename
cat /home/pi/Desktop/StevensBajaSAE/data/$new_filename > /home/pi/Desktop/StevensBajaSAE/data/current_data_file
cd /home/pi/Desktop/StevensBajaSAE
git add -A
git commit -m "added data files"
git push origin master
