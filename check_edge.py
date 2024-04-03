import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import shutil
from tqdm import tqdm
import traceback
import mediapipe as mp

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

def scale_bbox(bbox, scale_factor=1.2):
    x1, y1, x2, y2 = bbox
    w = x2 - x1
    h = y2 - y1
    
    new_w = w * scale_factor
    new_h = h * scale_factor
    
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    
    new_x1 = center_x - new_w / 2
    new_y1 = center_y - new_h / 2
    new_x2 = center_x + new_w / 2
    new_y2 = center_y + new_h / 2
    
    return int(new_x1), int(new_x2), int(new_y1), int(new_y2)

scores = np.zeros((range_shift*2, range_shift*2))  # Tạo một ma trận để lưu kết quả

path_folder = r'Photoface_dist\PhotofaceDB\1001\2008-02-23_12-21-31'

list_name_image = [x for x in os.listdir(path_folder) if x.endswith(".bmp")]

list_image = [(cv2.imread(os.path.join(path_folder, x))) for x in list_name_image]

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)

image = list_image[0]
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

landmark_points_68 = [168, 197, 5, 4, 75, 97, 2, 326, 305, 61, 39, 37, 0, 267, 269, 291, 405, 314, 17, 84, 181, 78, 82, 13, 312, 308, 317, 14, 87]

# Nhận dạng các điểm chấm trên khuôn mặt
bbox = [10000,0,10000,0]
results = face_mesh.process(image_rgb)
if results.multi_face_landmarks:
    for face_landmarks in results.multi_face_landmarks:
        # Vẽ các điểm chấm trên khuôn mặt
        print(len(face_landmarks.landmark))
        for index in range(len(face_landmarks.landmark)):
            if index in landmark_points_68:
                landmark = face_landmarks.landmark[index]
                x = int(landmark.x * image.shape[1])
                y = int(landmark.y * image.shape[0])
                bbox[0] = min(x,bbox[0])
                bbox[1] = max(x,bbox[1])
                bbox[2] = min(y,bbox[2])
                bbox[3] = max(y,bbox[3])

print(bbox)
bbox = scale_bbox(bbox, 2)
x1,x2,y1,y2 = tuple(bbox)
image = image[y1:y2,x1:x2,:]
cv2.imshow('check', image)

all_scores = []
max_shift = []
for i in range(len(list_image)):
    for j in range(len(list_image)):
        # pre_process ảnh
        image1 = list_image[i][y1:y2,x1:x2,:]
        image2 = list_image[j][y1:y2,x1:x2,:]

        threshold1 = 50
        threshold2 = 150
        edges1 = cv2.Canny(image1, threshold1, threshold2)
        edges2 = cv2.Canny(image2, threshold1, threshold2)

        crop_edges1 = edges1[range_shift:-range_shift, range_shift:-range_shift]
        max_score = 0
        best_x_shift, best_y_shift = 0,0
        scores = np.zeros((2*range_shift, 2*range_shift), dtype=int)  # Khởi tạo một mảng điểm số mới cho mỗi cặp ảnh
        for x_shift in range(-range_shift, range_shift):
            for y_shift in range(-range_shift, range_shift):
                edges_cal = edges2[range_shift+x_shift:-range_shift+x_shift, range_shift+y_shift:-range_shift+y_shift]
                score = count_common_edges(crop_edges1, edges_cal)
                scores[x_shift + range_shift][y_shift + range_shift] = score
                if score > max_score:
                    best_x_shift, best_y_shift = x_shift, y_shift
                    max_score = score
        # Thêm mảng điểm số này vào danh sách
        all_scores.append(scores)
        max_shift.append((best_x_shift, best_y_shift, max_score))

# Hiển thị tất cả các biểu đồ heatmap trong cùng một lần
fig, axs = plt.subplots(len(list_image), len(list_image), figsize=(10, 10))
for i in range(len(list_image)):
    for j in range(len(list_image)):
        axs[i, j].imshow(all_scores[i*len(list_image) + j], cmap='viridis', interpolation='nearest', extent=[-range_shift, range_shift, -range_shift, range_shift])
        axs[i, j].set_title(str(max_shift[i*len(list_image) + j]))
        # axs[i, j].set_xlabel('Dịch chuyển theo x')
        # axs[i, j].set_ylabel('Dịch chuyển theo y')

# Thêm colorbar
# fig.colorbar(axs[0, 0].imshow(all_scores[0], cmap='viridis', interpolation='nearest', extent=[-range_shift, range_shift, -range_shift, range_shift]), ax=axs, orientation='vertical', fraction=0.05, pad=0.04)

# Hiển thị biểu đồ
plt.suptitle('Biểu đồ heatmap của các bảng điểm số')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()