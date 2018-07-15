#!/usr/bin/env python3

import pygame.camera
import numpy as np
import subprocess
from time import sleep, time
from datetime import datetime
import config
from sklearn.ensemble import RandomForestRegressor
from scipy.misc import imresize
from sklearn.externals import joblib
import os


def get_img():
    '''Gets webcam image and returns it as array

    Returns
    -------
    ndarray
        image taken by webcam
    '''
    print("detecting brightness")
    pygame.camera.init()
    cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
    cam.start()
    img = cam.get_image()
    cam.stop()
    imgdata = pygame.surfarray.array3d(img)
    return imgdata


def change_brightness(val: int):
    '''Changes screen brightbess

    Parameters
    ----------
    val: int
        value between 0 and 100
        100 -> maximum brightness is set'''
    cmd = config.backlight_cmd
    if config.block_zero_brightness:
        val += 1
    val = str(int(val))
    subprocess.call([
        cmd,
        "-time",
        str(config.xb_time),
        "-steps",
        str(config.xb_steps),
        "-set",
        val])


def get_brightness():
    """Reads current brighness

    Returns
    -------
    int
        current brighness
    """
    cmd = config.backlight_cmd
    cmd = " ".join([cmd, "-get"])
    process = subprocess.Popen(cmd, shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    # wait for the process to terminate
    out, err = process.communicate()
    return int(out)


def preprocess(img: np.ndarray, res=4):
    """Resizes and flattens image

    Parameters
    ----------
    img : np.ndarray
        image to process
    res : int, optional
        image is resized to shape=(res,res) (the default is 4)

    Returns
    -------
    np.ndarray
        flattened image
    """

    img = imresize(img, size=(res, res), interp="lanczos")
    img = np.mean(img, axis=2)
    img = img.flatten()
    return img


def infos():
    '''Additional infos of current time

    Returns
    -------
    list:
        [mont, weekday, hour]
    '''
    d = datetime.today()
    month = d.month
    weekday = d.weekday()
    hour = d.hour
    return [month, weekday, hour]


def gen_x():
    '''Generates sample to be learned

    Returns
    -------
    ndarray
        processed image data and
        additional infos
    '''
    img = get_img()
    img_p = preprocess(img)
    x = np.append(img_p, infos())
    return x


def gen_y():
    '''Generates preferred sample output

    Returns
    -------
    ndarray
        brightness'''
    return np.array([get_brightness()])


def main():
    '''Updates the screen brightness'''
    clf = joblib.load(filename)
    prev_val = 1000
    while True:
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
    '''Collects samples to be used by machine learner

    Notes
    -----
    Saves ndarrays to ./traindata/
    '''
    directory = localpath + "/traindata/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    while True:
        x = gen_x()
        y = gen_y()
        np.save(directory + "XY" +
                str(time()) + ".npy", np.array([x, y]))
        sleep(config.sleep)


def dummy():
    pass


def fit():
    '''Fits a RandomForest to the traindata

    Notes
    -----
    Use aquire_data() before fitting
    in order to generate the trainingsset
    '''
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
    clf = joblib.load(filename)
    imps = clf.feature_importances_
    print("brighness importance %d perc." % (np.sum(imps[:-3]) * 100))
    print("month importance %d perc." % (imps[-3] * 100))
    print("weekday importance %d perc." % (imps[-2] * 100))
    print("hour importance %d perc." % (imps[-1] * 100))
    # pass
