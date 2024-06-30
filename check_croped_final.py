import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import shutil
from tqdm import tqdm
import traceback

range_shift = 20

def pre_process(image):
    # blurred_image = cv2.GaussianBlur(image, (5, 5), 0)

    # # Tách các kênh màu
    # b, g, r = cv2.split(blurred_image)

    # # Cân bằng sáng cho từng kênh màu
    # equalized_b = cv2.equalizeHist(b)
    # equalized_g = cv2.equalizeHist(g)
    # equalized_r = cv2.equalizeHist(r)

    # # Ghép các kênh màu đã cân bằng sáng lại thành ảnh màu
    # equalized_image = cv2.merge((equalized_b, equalized_g, equalized_r))
    equalized_image = adjust_gamma(image, 1.2)
    # equalized_image = cv2.GaussianBlur(equalized_image, (5, 5), 0)
    return equalized_image

def histogram_equalization(image):
    # Chuyển ảnh về ảnh xám nếu ảnh màu
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Cân bằng histogram
    equalized_image = cv2.equalizeHist(image)
    
    return equalized_image

def adjust_gamma(image, gamma=1.0):
    # Build a lookup table mapping the pixel values [0, 255] to their adjusted gamma values
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    
    # Apply gamma correction using the lookup table
    return cv2.LUT(image, table)

def count_common_edges(edges1, edges2):
    common_edges = cv2.bitwise_and(edges1, edges2)
    contours, _ = cv2.findContours(common_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    num_common_edges = 0
    for contour in contours:
        if len(contour) >= 5:
            num_common_edges += len(contour)
    return num_common_edges

scores = np.zeros((range_shift*2, range_shift*2))  # Tạo một ma trận để lưu kết quả

def cal_crop_shift(image1, image2):
    # image1 = histogram_equalization(image1)
    # image2 = histogram_equalization(image2)
    threshold1 = 50
    threshold2 = 250
    gamma = 1
    image1 = adjust_gamma(image1, 1)
    image2 = adjust_gamma(image2, 1)    
    edges1 = cv2.Canny(image1, threshold1, threshold2)
    edges2 = cv2.Canny(image2, threshold1, threshold2)

    crop_edges1 = edges1[range_shift:-range_shift, range_shift:-range_shift]
    max_score = 0
    best_x_shift, best_y_shift = 0,0
    for x_shift in range(-range_shift, range_shift):
        for y_shift in range(-range_shift, range_shift):
            edges_cal = edges2[range_shift+x_shift:-range_shift+x_shift, range_shift+y_shift:-range_shift+y_shift]
            # common_edges = cv2.bitwise_and(crop_edges1, edges_cal)
            # score = cv2.countNonZero(common_edges)
            score = count_common_edges(crop_edges1, edges_cal)
            scores[x_shift + range_shift][y_shift + range_shift] = score
            if score > max_score:
                best_x_shift, best_y_shift = x_shift, y_shift
                max_score = score
    im1_crop = image1[range_shift:-range_shift, range_shift:-range_shift, :]
    im2_crop = image2[range_shift+best_x_shift:-range_shift+best_x_shift, range_shift+best_y_shift:-range_shift+best_y_shift, :]
    return max_score, best_x_shift, best_y_shift, im1_crop, im2_crop

