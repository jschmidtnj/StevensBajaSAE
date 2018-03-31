xinput --set-prop 'FT5406 memory based driver' 'Coordinate Transformation Matrix' 0 1 0 -1 0 1 0 0 1
cd /home/pi/Desktop/StevensBajaSAE
git pull origin master
git add -A
git commit -m "added data files"
git push origin master
python3 /home/pi/Desktop/StevensBajaSAE/app-1.py