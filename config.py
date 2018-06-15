#!/usr/bin/env python3

# command to backlight or xbacklight
backlight_path = \
    "/home/simtron/Documents/Python/acpilight/xbacklight"
xb_time = 5000  # milliseconds to switch brightness, xbacklight time
xb_steps = 5 * 25  # steps to change brightness, xbacklight steps
update_threshold = 5 # ignore changing brightness when it difference is under threshold
sleep = 10  # seconds, time between photo detection
