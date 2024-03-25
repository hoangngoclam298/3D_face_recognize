import cv2
import mediapipe as mp
import matplotlib.pyplot as plt

# Khởi tạo đối tượng Mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)

# Đọc ảnh
image = cv2.imread(r'Photoface_dist\PhotofaceDB\1001\2008-02-23_12-21-31\im3.bmp')
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# list_point = [61, 146, 146, 91, 91, 181, 181, 84, 84, 17, 17, 314, 314, 405, 405, 321,
# 321, 375, 375, 291, 61, 185, 185, 40, 40, 39, 39, 37, 37, 0, 0, 267, 267,
# 269, 269, 270, 270, 409, 409, 291, 78, 95, 95, 88, 88, 178, 178, 87, 87, 14,
# 14, 317, 317, 402, 402, 318, 318, 324, 324, 308, 78, 191, 191, 80, 80, 81,
# 81, 82, 82, 13, 13, 312, 312, 311, 311, 310, 310, 415, 415, 308, 1]

# landmark_points_68 = [162,234,93,58,172,136,149,148,152,377,378,365,397,288,323,454,389,71,63,105,66,107,336,
#                   296,334,293,301,168,197,5,4,75,97,2,326,305,33,160,158,133,153,144,362,385,387,263,373,
#                   380,61,39,37,0,267,269,291,405,314,17,84,181,78,82,13,312,308,317,14,87]

# nose_and_lip = [x for x in range(68) if (x>26 and x<36) or (x>47 and x<68)]
# landmark_points_68_new = [landmark_points_68[index] for index in nose_and_lip]
# print(landmark_points_68_new)
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
x1,x2,y1,y2 = tuple(bbox)

# # Hiển thị ảnh với các điểm chấm
# cv2.imshow('Face Landmarks', image[y1:y2,x1:x2,:])
# cv2.waitKey(0)
# cv2.destroyAllWindows()

image = image[y1:y2,x1:x2,:]
edges = cv2.Canny(image, threshold1=100, threshold2=200)  # Điều chỉnh ngưỡng tùy ý
print(edges[20:-20,20:-20].shape)

# Hiển thị ảnh gốc và ảnh sau khi phát hiện cạnh
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(image, cmap='gray')
plt.title('Ảnh gốc')
plt.subplot(1, 2, 2)
plt.imshow(edges, cmap='gray')
plt.title('Cạnh phát hiện (Canny)')
plt.show()
