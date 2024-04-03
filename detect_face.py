import cv2
import mediapipe as mp
import os
from tqdm import tqdm

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
    return faces


path_folder = r'C:\Users\LAMHN\Documents\DoAn_KiSu\Photoface_dist\PhotofaceDB'
crop_path_folder = r'C:\Users\LAMHN\Documents\DoAn_KiSu\cropped_data'
list_folder_id = [x for x in os.listdir(path_folder) if os.path.isdir(os.path.join(path_folder, x))]
list_image_path = []

for id in tqdm(list_folder_id):
    path_folder_id = os.path.join(path_folder, id)
    list_folder_id_time = [x for x in os.listdir(path_folder_id) if os.path.isdir(os.path.join(path_folder_id ,x))]
    for time_id in list_folder_id_time:
        path_folder_id_time = os.path.join(path_folder_id, time_id)
        list_name_image = [x for x in os.listdir(path_folder_id_time) if x.endswith(".bmp")]
        list_image_path.append(os.path.join(path_folder_id_time, list_name_image[0]))

# Lặp qua từng đường dẫn ảnh
for image_path in list_image_path:
    # Đọc ảnh từ đường dẫn
    image = cv2.imread(image_path)
    
    # Detect khuôn mặt và lấy toạ độ bounding box
    detected_faces = detect_faces(image)
    
    # Vẽ bounding box lên ảnh gốc
    for bbox in detected_faces:
        cv2.rectangle(image, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (0, 255, 0), 2)

    # Hiển thị ảnh với bounding box
    cv2.imshow("Detected Faces", image)
    cv2.waitKey(200)  # Chờ 1 giây
    cv2.destroyAllWindows()

    # Để chắc chắn rằng cửa sổ hiển thị ảnh được đóng trước khi hiển thị ảnh tiếp theo
    while cv2.getWindowProperty("Detected Faces", cv2.WND_PROP_VISIBLE) >= 1:
        cv2.waitKey(50)  # Chờ 50ms
