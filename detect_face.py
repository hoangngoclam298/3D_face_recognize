import cv2
import mediapipe as mp

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

if __name__ == "__main__":
    # Đọc ảnh đầu vào
    image = cv2.imread("im1.bmp")

    # Detect khuôn mặt và lấy toạ độ bounding box
    detected_faces = detect_faces(image)

    # Vẽ bounding box lên ảnh gốc
    for bbox in detected_faces:
        print(bbox)
        cv2.rectangle(image, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (0, 255, 0), 2)

    # Hiển thị ảnh với bounding box
    cv2.imshow("Detected Faces", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
