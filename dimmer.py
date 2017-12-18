#!/usr/bin/env python3

import pygame.camera
import numpy as np
import subprocess
import time
import config


def get_img():
    '''gets webcam image and returns it as array'''
    pygame.camera.init()
    cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
    cam.start()
    img = cam.get_image()
    cam.stop()
    imgdata = pygame.surfarray.array3d(img)
    return imgdata


def change_brightness(val):
    '''val: int, 0=< val <= 100'''
    acpilight_path = config.backlight_path
    val = str(int(val))
    subprocess.call([acpilight_path, "-time", str(config.xb_time),
                     "-steps", str(config.xb_steps), "-set", val])


def weight_img(img):
    img = 3 * np.mean(img) / 170 * 100
    return int(img)


def main():
    prev_vals = [100]
    prev_mean = None
    while True:
        try:
            img_val = weight_img(get_img())
            # if deviation is high, reset prev_vals
            if abs(img_val - np.mean(prev_vals)) > 20:
                prev_vals = [img_val]
            else:
                prev_vals.append(img_val)
            # smooth by last values to prevent oscillation of brightness
            if len(prev_vals) < (config.averaging - 1):
                prev_vals = prev_vals[:(config.averaging - 1)]

            val_mean = int(np.mean(prev_vals))
            # only steps by 10 to prevent changing the
            # brightness in every evaluation
            if val_mean > config.sensible_threshold:
                val_mean = int(val_mean // config.steps * config.steps)
            # do not disable screen light
            elif val_mean < config.low_threshold:
                val_mean = config.low_light
            print("setting brigness to", val_mean)
            if prev_mean != val_mean:
                change_brightness(val_mean)
                prev_mean = val_mean
        except SystemError:
            print("Camera blocked by other Programm")
        time.sleep(config.sleep)


if __name__ == "__main__":
    main()
