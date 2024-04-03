import cv2
import mediapipe as mp

# Khởi tạo đối tượng Mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)

# Đọc ảnh
image = cv2.imread(r'Photoface_dist\PhotofaceDB\1001\2008-02-23_12-21-31\im0.bmp')
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

list_point = [168, 197, 5, 4, 75, 97, 2, 326, 305, 61, 39, 37, 0, 267, 269, 291, 405, 314, 17, 84, 181, 78, 82, 13, 312, 308, 317, 14, 87]


# Nhận dạng các điểm chấm trên khuôn mặt
results = face_mesh.process(image_rgb)
if results.multi_face_landmarks:
    for face_landmarks in results.multi_face_landmarks:
        # Vẽ các điểm chấm trên khuôn mặt
        print(len(face_landmarks.landmark))
        for index in range(len(face_landmarks.landmark)):
            # if index in list_point:
                landmark = face_landmarks.landmark[index]
                x = int(landmark.x * image.shape[1])
                y = int(landmark.y * image.shape[0])
                cv2.circle(image, (x, y), 2, (0, 255, 0), -1)

# Hiển thị ảnh với các điểm chấm
cv2.imshow('Face Landmarks', image)
cv2.waitKey(0)
cv2.destroyAllWindows()