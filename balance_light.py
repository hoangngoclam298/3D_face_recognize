import cv2

# Đọc ảnh
image = cv2.imread('im0.bmp')

# Chuyển đổi ảnh sang ảnh đen trắng
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Cân bằng độ sáng tự adapt
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
clahe_image = clahe.apply(gray_image)

# Hiển thị ảnh gốc và ảnh đã cân bằng độ sáng
cv2.imshow('Original Image', gray_image)
cv2.imshow('CLAHE Image', clahe_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
