import cv2

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

image = []
image.append(cv2.imread('im0.bmp'))
image.append(cv2.imread('im1.bmp'))
image.append(cv2.imread('im2.bmp'))
image.append(cv2.imread('im3.bmp'))

for x in range(4):
    for y in range(4):
        print(f"im{x} + im{y} = {compute_image_sharpness((image[x]*0.5+0.5*image[y]))}")
