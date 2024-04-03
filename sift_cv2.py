import cv2
import numpy as np
import mediapipe as mp

# Hàm thu nhỏ bbox
def scale_bbox(bbox, scale_factor=1.2):
    x1, x2, y1, y2 = bbox
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

# Khởi tạo đối tượng SIFT
sift = cv2.SIFT_create()

# Đọc ảnh và thu nhỏ bbox
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)

images = []
landmark_points_68 = [168, 197, 5, 4, 75, 97, 2, 326, 305, 61, 39, 37, 0, 267, 269, 291, 405, 314, 17, 84, 181, 78, 82, 13, 312, 308, 317, 14, 87]

image = cv2.imread('im0.bmp')
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

bbox = [10000, 0, 10000, 0]
results = face_mesh.process(image_rgb)
if results.multi_face_landmarks:
    for face_landmarks in results.multi_face_landmarks:
        for index in range(len(face_landmarks.landmark)):
            if index in landmark_points_68:
                landmark = face_landmarks.landmark[index]
                x = int(landmark.x * image.shape[1])
                y = int(landmark.y * image.shape[0])
                bbox[0] = min(x, bbox[0])
                bbox[1] = max(x, bbox[1])
                bbox[2] = min(y, bbox[2])
                bbox[3] = max(y, bbox[3])

bbox = scale_bbox(bbox, 1.5)
x1, x2, y1, y2 = tuple(bbox)

for i in range(4):
    image = cv2.imread(f'im{i}.bmp')
    image = image[y1:y2, x1:x2, :]
    images.append(image)

# Gộp các ảnh lại thành một ảnh duy nhất
merged_image = np.concatenate(images, axis=1)

# Tìm keypoint và descriptors
keypoints, descriptors = sift.detectAndCompute(merged_image, None)

# Vẽ các keypoint lên ảnh
image_with_keypoints = cv2.drawKeypoints(merged_image, keypoints, None)

# Hiển thị ảnh với các keypoint
cv2.imshow('Image with SIFT Keypoints', image_with_keypoints)
cv2.waitKey(0)
cv2.destroyAllWindows()
