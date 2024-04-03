import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt

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
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
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

def scale_bbox(bbox, scale_factor=1.2):
    x, y, w, h = bbox
    new_w = w * scale_factor
    new_h = h * scale_factor
    new_x = x - (new_w - w) / 2
    new_y = y - (new_h - h) / 2
    return int(new_x), int(new_y), int(new_w), int(new_h)

def pre_process(image):
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

# im0 = pre_process(cv2.imread('im0.bmp'))
# im3 = pre_process(cv2.imread('im3.bmp'))

im0 = cv2.imread('im0.bmp')
im3 = cv2.imread('im3.bmp')

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)

image = im0
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
print(bbox)

bbox = scale_bbox(bbox, 1)
x1,x2,y1,y2 = tuple(bbox)
x,y,w,h = x1,y1,x2-x1,y2-y1
bbox = (x,y,w,h)
# bbox = detect_faces(im0)
# # bbox = scale_bbox(bbox)
# x,y,w,h = bbox

crop_im0 = im0[y:y+w,x:x+h,:]

range_shift = 20 
max_score = 0
scores = np.zeros((range_shift*2, range_shift*2))  # Tạo một ma trận để lưu kết quả

for x_shift in range(-range_shift, range_shift):
    for y_shift in range(-range_shift, range_shift):
        img_tmp = merge_image_v2(crop_im0, im3, bbox, (x_shift, y_shift))
        score_tmp = cal_sharpness_v1(img_tmp)
        scores[x_shift + range_shift][y_shift + range_shift] = score_tmp
        if score_tmp > max_score:
            max_score = score_tmp
            best_x_shift, best_y_shift = x_shift, y_shift

print("Điểm số cao nhất:", max_score)
print("X Shift tốt nhất:", best_x_shift)
print("Y Shift tốt nhất:", best_y_shift)
re_2image(crop_im0, im3, bbox, (best_x_shift, best_y_shift))


plt.imshow(scores, cmap='viridis', interpolation='nearest', extent=[-range_shift, range_shift, -range_shift, range_shift])
plt.colorbar(label='Điểm số')
plt.title('Biểu đồ heatmap của hàm score')
plt.xlabel('Dịch chuyển theo x')
plt.ylabel('Dịch chuyển theo y')
plt.show()
