import cv2
import mediapipe as mp
import numpy as np
import math

def gray_to_3_channels(gray_image):
    # Tạo ba kênh màu giống nhau từ ảnh xám ban đầu
    blue_channel = gray_image.copy()
    green_channel = gray_image.copy()
    red_channel = gray_image.copy()

    # Ghép ba kênh màu lại thành ảnh màu
    merged_image = cv2.merge([blue_channel, green_channel, red_channel])

    return merged_image

def bmp_equalization(image):
    # Chuyển đổi ảnh sang ảnh xám
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Bi-histogram equalization
    hist, bins = np.histogram(gray_image.flatten(), 256, [0,256])
    cdf = hist.cumsum()
    cdf_masked = np.ma.masked_equal(cdf, 0)
    cdf_masked = (cdf_masked - cdf_masked.min())*255/(cdf_masked.max()-cdf_masked.min())
    cdf = np.ma.filled(cdf_masked, 0).astype('uint8')

    equalized_image = cdf[gray_image]

    return gray_to_3_channels(equalized_image)

def euclidean_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def eval_2landmark(landmark1, landmark2):
    vector_distance = []
    for index in range(len(landmark1)):
        vector_distance.append(euclidean_distance(landmark1[index], landmark2[index]))
    return np.linalg.norm(vector_distance, ord=2)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

all_indices = list(range(145, 159)) + list(range(372, 386)) + list(range(1, 244)) + list(range(61, 291))
list_oval = [61, 146, 146, 91, 91, 181, 181, 84, 84, 17, 17, 314, 314, 405, 405, 321,
321, 375, 375, 291, 61, 185, 185, 40, 40, 39, 39, 37, 37, 0, 0, 267, 267,
269, 269, 270, 270, 409, 409, 291, 78, 95, 95, 88, 88, 178, 178, 87, 87, 14,
14, 317, 317, 402, 402, 318, 318, 324, 324, 308, 78, 191, 191, 80, 80, 81,
81, 82, 82, 13, 13, 312, 312, 311, 311, 310, 310, 415, 415, 308]

def get_landmark(file_path):
    global face_mesh
    if face_mesh is not None:
        face_mesh.close()
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

    image = bmp_equalization(cv2.imread(file_path))
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)
    landmarkre = []
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for index in range(len(face_landmarks.landmark)):
                if index in list_oval:
                    x,y = face_landmarks.landmark[index].x, face_landmarks.landmark[index].y
                    image_height, image_width, _ = image.shape
                    x = (x * image_width)
                    y = (y * image_height)
                    landmarkre.append((x,y))
    return landmarkre

landmark1 = get_landmark('im0.bmp')
print(len(landmark1))
landmark2 = get_landmark('im3.bmp')

def shift_landmark(landmark, shift_tmp):
    landmark_re = []
    x,y = shift_tmp
    for xt, yt in landmark:
        landmark_re.append((xt+x, yt+y))
    return landmark_re

def result_new_shift(shift_tmp):
    x, y = shift_tmp
    return [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]

dict_shift = {(0,0):eval_2landmark(landmark1, landmark2)}
shift_best = (0,0)
best_value = dict_shift[(0,0)]
visited = []
dict_fail = {}

while len(dict_shift) > 0 or len(dict_fail) > 0:
    while len(dict_shift) > 0:
        shift_tmp, value_shift = dict_shift.popitem()        
        new_shift = result_new_shift(shift_tmp)
        for tmp_shift in new_shift:
            if tmp_shift in visited:
                continue
            new_value = eval_2landmark(landmark1, shift_landmark(landmark2, tmp_shift))
            visited.append(tmp_shift)
            if new_value < value_shift:
                dict_shift[tmp_shift] = new_value
                if new_value < best_value:
                    best_value = new_value
                    shift_best = tmp_shift
            else:
                dict_fail[tmp_shift] = value_shift
    
    while len(dict_fail) > 0:
        shift_tmp, value_shift = dict_fail.popitem()        
        new_shift = result_new_shift(shift_tmp)
        for tmp_shift in new_shift:
            if tmp_shift in visited:
                continue
            new_value = eval_2landmark(landmark1, shift_landmark(landmark2, tmp_shift))
            visited.append(tmp_shift)
            if new_value < value_shift:
                dict_shift[tmp_shift] = new_value
                if new_value < best_value:
                    best_value = new_value
                    shift_best = tmp_shift

print(shift_best, best_value)


landmarks1 = np.array(landmark1).astype(int)
landmarks2 = np.array(landmark2).astype(int)

image = cv2.imread(r'C:\Users\LAMHN\Documents\DoAn_KiSu\im3.bmp')

for landmark in landmarks1:
    cv2.circle(image, tuple(landmark), 2, (0, 0, 255), -1)  # Đỏ

for landmark in landmarks2:
    cv2.circle(image, tuple(landmark), 2, (255, 0, 0), -1)  # Xanh

# Hiển thị ảnh
cv2.imshow('Landmarks', image)
cv2.waitKey(0)
cv2.destroyAllWindows()



