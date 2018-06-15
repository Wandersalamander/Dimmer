#!/usr/bin/env python3

import pygame.camera
import numpy as np
import subprocess
from time import sleep, time
from datetime import date
from datetime import datetime
import config
from sklearn.ensemble import RandomForestRegressor
from scipy.misc import imresize
from sklearn.externals import joblib
import os


def get_img():
    '''gets webcam image and returns it as array'''
    print("detecting brightness")
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
    subprocess.call([
        acpilight_path,
        "-time",
        str(config.xb_time),
        "-steps",
        str(config.xb_steps),
        "-set",
        val])


def get_brightness():
    '''val: int, 0=< val <= 100'''
    acpilight_path = config.backlight_path
    cmd = " ".join([acpilight_path, "-get"])
    process = subprocess.Popen(cmd, shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    # wait for the process to terminate
    out, err = process.communicate()
    return int(out)


def preprocess(img, res=4):
    '''Returns flat ndarray'''
    img = imresize(img, size=(res, res), interp="lanczos")
    img = np.mean(img, axis=2)
    img = img.flatten()
    return img


def infos():
    d = datetime.today()
    month = d.month
    weekday = d.weekday()
    hour = d.hour
    return [month, weekday, hour]


def gen_x():
    img = get_img()
    img_p = preprocess(img)
    x = np.append(img_p, infos())
    return x


def gen_y():
    return np.array([get_brightness()])


def main():
    clf = joblib.load(filename)
    loop_count = 0
    prev_val = 1000
    while True:
        loop_count += 1
        try:
            x = gen_x()
            val = clf.predict([x])[0]
            dif = np.abs(val - prev_val)
            if dif > config.update_threshold:
                print("setting brigness to", val)
                change_brightness(val)
                prev_val = val
            else:
                print("difference below %d, brighness not changed" %
                      config.update_threshold)
        except SystemError:
            print("Camera blocked by other Programm")
        sleep(config.sleep)


def aquire_data():
    while True:
        x = gen_x()
        y = gen_y()
        np.save(localpath + "/traindata/XY" + str(time()) + ".npy", np.array([x, y]))
        sleep(config.sleep)


def dummy():
    pass


def fit():
    clf = RandomForestRegressor()
    X, Y = [], []
    path = localpath + "/traindata/"
    for file in os.listdir(path):
        xy = np.load(path + file)
        X.append(xy[0])
        Y.append(xy[1][0])
    X = np.array(X)
    Y = np.array(Y)
    clf.fit(X, Y)
    joblib.dump(clf, filename)


localpath = __file__.replace(os.path.basename(__file__), "")
filename = localpath + 'RandomForestRegressor.pkl'
if __name__ == "__main__":
    # aquire_data()
    pass
    # train()
    # main()
