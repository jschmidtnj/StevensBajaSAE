xinput --set-prop 'FT5406 memory based driver' 'Coordinate Transformation Matrix' 0 1 0 -1 0 1 0 0 1
sudo su
brightness=100
echo $brightness > /sys/class/backlight/rpi_backlight/brightness
exit