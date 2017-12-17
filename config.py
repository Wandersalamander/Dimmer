#!/usr/bin/env python3

# path to backlight or xbacklight
backlight_path = "/home/simtron/Documents/Python/acpilight/xbacklight"
xb_time = 1000  # milliseconds, xbacklight time
xb_steps = 25  # xbacklight steps

sleep = 10  # seconds, time between photo detection

averaging = 10  # last n photos to be considered

averaging_ignore = 20  # jump to measured brigthness
# if differenc to average brighness is higher than this value
# for example:
# average = 30, measured = 80
# -> 80 - 30 > 20 (averaging_ignore)
# -> set brightness to 80

steps = 10  # int, steps in which the light is changed,
# for example: brightness 30, 40, 50, .. for steps = 10
sensible_threshold = 20  # under this value steps will be ignored

low_threshold = 5  # all light values under threshold will be set to low_light
low_light = 3  # lowest light value
