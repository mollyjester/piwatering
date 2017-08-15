pgrep pigpiod > /dev/null || sudo pigpiod
python3 /home/pi/python/watering/pump_only.py
