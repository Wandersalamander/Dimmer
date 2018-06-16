Programm to automatically controll your screen brightness.
It can learn your brightness preferences depending on
the environment brightness, time and date and then
use set the brighness for your.

On some machines acpilight is required to set the brighness
https://github.com/wavexx/acpilight

## appindicator.py:

    Starts dimmer and adds an appindicator to the taskbar,
    you may add this to the autostart

## dimmer.py:

    Core script to autocontroll the brighness, no flags supported
    but config.py available to set preferences

## config.py:
    user preferences
    set the path to the programm editing your brightness here
    in order to make the programm work

# Notes
## Learning
Dimmer comes with a pretrained regressor.
If you start to train your regressor, the pretrained regressor
is going to be neglected and a new regressor ist trained on
all data contained in /traindata/.
## Installation
Make sure you have installed backlight, xbacklight or acpibacklight or another programm which supports the flags
    -time
    -steps
    -set
    -get
and paste the command into the config.py file.

all modules are testet on ubuntu 18.04
