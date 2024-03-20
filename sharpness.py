from PIL import Image
import numpy as np

import cv2

def merge_image(image1, image2):
    if image1.shape == image2.shape:
        blended_image = cv2.addWeighted(image1, 0.5, image2, 0.5, 0)
        return cv2.cvtColor(blended_image, cv2.COLOR_BGR2GRAY)

def cal_sharpness_v1(gray):
    gy, gx = np.gradient(gray)
    gnorm = np.sqrt(gx**2 + gy**2)
    sharpness = np.average(gnorm)
    return sharpness

def cal_sharpness_v2(gray):
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    mean, std_dev = cv2.meanStdDev(laplacian)
    sharpness = std_dev[0] ** 2
    return sharpness


