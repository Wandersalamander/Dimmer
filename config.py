#!/usr/bin/env python3

# command to backlight or xbacklight
backlight_path = "/home/simtron/Documents/Python/acpilight/xbacklight"
# milliseconds to switch brightness, (argument passed to xbacklight)
xb_time = 1000
xb_steps = 25  # steps to change brightness, xbacklight steps

sleep = 10  # seconds, time between photo detection

averaging = 10  # last n photos to be considered

######
# as backlight and xbacklight change their values between 0 and 100
# following brigthness values applie to these borders
######

jump_theshold = 20  # jump to measured brigthness if
# differenc to average brighness is higher than this value
# for example:
# average = 30, measured = 80
# -> 80 - 30 > 20 (averaging_ignore)
# -> set brightness to 80

steps = 10  # int, steps in which the light is changed,
# for example: brightness 30, 40, 50, .. for steps = 10
sensible_threshold = 20  # under this value steps will be ignored
# for example:
# ..,5,6,7,8,9,10,20,30,40,.. for steps=10 and sensible_threshold = 10

low_threshold = 5  # all light values under threshold will be set to low_light
low_light = 3  # lowest light value
