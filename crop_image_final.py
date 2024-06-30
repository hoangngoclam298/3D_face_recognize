import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
import os

def detect_faces(image):
    mp_face_detection = mp.solutions.face_detection
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    with mp_face_detection.FaceDetection(min_detection_confidence=0.7) as face_detection:
        results = face_detection.process(image_rgb)
        faces = []
        if results.detections:
            for detection in results.detections:
                ih, iw, _ = image.shape
                bboxC = detection.location_data.relative_bounding_box
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih),\
                       int(bboxC.width * iw), int(bboxC.height * ih)
                faces.append(bbox)
    return faces[0]

def merge_image(image1, image2):
    if image1.shape == image2.shape:
        blended_image = cv2.addWeighted(image1, 0.5, image2, 0.5, 0)
        return cv2.cvtColor(blended_image, cv2.COLOR_BGR2GRAY)

def merge_image_v2(image1, image2, bbox, shift):
    x,y,w,h = bbox
    x_shift, y_shift = shift
    x += x_shift
    y += y_shift
    image2 = image2[y:y+w,x:x+h,:]
    if image1.shape == image2.shape:
        blended_image = cv2.addWeighted(image1, 0.5, image2, 0.5, 0)
        return cv2.cvtColor(blended_image, cv2.COLOR_BGR2GRAY)

def re_2image(image1, image2, bbox, shift):
    x,y,w,h = bbox
    x_shift, y_shift = shift
    x += x_shift
    y += y_shift
    image2 = image2[y:y+w,x:x+h,:]
    if image1.shape == image2.shape:
        cv2.imwrite('result1.png', image1)
        cv2.imwrite('result2.png', image2)

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

def cal_sharpness_v3(image1, image2, bbox, shift):
    x,y,w,h = bbox
    x_shift, y_shift = shift
    x += x_shift
    y += y_shift
    image2 = image2[y:y+w,x:x+h,:]
    if image1.shape == image2.shape:    
        edges1 = cv2.Canny(image1, threshold1=100, threshold2=200)
        edges2 = cv2.Canny(image2, threshold1=100, threshold2=200)
        common_edges = cv2.bitwise_and(edges1, edges2)
        return cv2.countNonZero(common_edges)

def scale_bbox(bbox, scale_factor=1.2):
    x, y, w, h = bbox
    new_w = w * scale_factor
    new_h = h * scale_factor
    new_x = x - (new_w - w) / 2
    new_y = y - (new_h - h) / 2
    return int(new_x), int(new_y), int(new_w), int(new_h)

def pre_process1(image):
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)

    # Tách các kênh màu
    b, g, r = cv2.split(blurred_image)

    # Cân bằng sáng cho từng kênh màu
    equalized_b = cv2.equalizeHist(b)
    equalized_g = cv2.equalizeHist(g)
    equalized_r = cv2.equalizeHist(r)

    # Ghép các kênh màu đã cân bằng sáng lại thành ảnh màu
    equalized_image = cv2.merge((equalized_b, equalized_g, equalized_r))
    return equalized_image

def adjust_gamma(image, gamma=1.0):
    # Build a lookup table mapping the pixel values [0, 255] to their adjusted gamma values
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    
    # Apply gamma correction using the lookup table
    return cv2.LUT(image, table)


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
    equalized_image = adjust_gamma(image, 1.5)
    # equalized_image = cv2.GaussianBlur(equalized_image, (5, 5), 0)
    return equalized_image

path_folder = r'C:\Users\LAMHN\Documents\DoAn_KiSu'
list_image = os.listdir(path_folder)
list_image = [x for x in list_image if x.endswith(".bmp")]

for name_image0 in list_image:
    im0 = pre_process(cv2.imread(os.path.join(path_folder, name_image0)))

    bbox = detect_faces(im0)
    bbox = scale_bbox(bbox, 1.0)
    x,y,w,h = bbox
    crop_im0 = im0[y:y+w,x:x+h,:]

    range_shift = 20
    result_check = {}

    for name_image in list_image:
        max_score = 0
        best_x_shift, best_y_shift = 0,0
        im_check = pre_process(cv2.imread(os.path.join(path_folder, name_image)))
        for x_shift in range(-range_shift, range_shift):
            for y_shift in range(-range_shift, range_shift):
                img_tmp = merge_image_v2(crop_im0, im_check, bbox, (x_shift, y_shift))
                score_tmp = cal_sharpness_v1(img_tmp)
                # score_tmp = cal_sharpness_v3(crop_im0, im_check, bbox, (x_shift, y_shift))
                if score_tmp > max_score:
                    max_score = score_tmp
                    best_x_shift, best_y_shift = x_shift, y_shift
        result_check[name_image] = (best_x_shift, best_y_shift, max_score)

    print(name_image0, result_check)
