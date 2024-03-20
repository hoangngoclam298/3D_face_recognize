import cv2
import numpy as np

def new_image(path1, path2):
    image1 = cv2.imread(path1)
    # Load ảnh thứ hai
    image2 = cv2.imread(path2)

    # Kiểm tra xem hai ảnh có cùng kích thước không
    if image1.shape == image2.shape:
        # Gộp hai ảnh lại với nhau và tính toán giá trị trung bình của từng pixel
        blended_image = cv2.addWeighted(image1, 0.5, image2, 0.5, 0)
        return blended_image

# Định nghĩa hàm tính toán độ sắc nét của ảnh
def compute_image_sharpness(image):
    # Chuyển ảnh sang ảnh grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Sử dụng bộ lọc Laplacian để tính gradient
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    
    # Tính toán giá trị trung bình và độ lệch chuẩn của gradient
    mean, std_dev = cv2.meanStdDev(laplacian)
    
    # Tính toán độ sắc nét dựa trên độ lệch chuẩn
    sharpness = std_dev[0] ** 2
    
    return sharpness

# Đọc ảnh
image = cv2.imread('im0.bmp')
image = new_image('im0.bmp','im3.bmp')

# Tính toán độ sắc nét của ảnh
sharpness = compute_image_sharpness(image)

# Hiển thị kết quả
print("Độ sắc nét của ảnh:", sharpness)
