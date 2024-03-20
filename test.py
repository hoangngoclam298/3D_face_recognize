import cv2
import numpy as np
import matplotlib.pyplot as plt

# Đọc ảnh
def pre_process(image):
    image = cv2.GaussianBlur(image, (5, 5), 0)

    # Tách các kênh màu
    b, g, r = cv2.split(image)

    # Cân bằng sáng cho từng kênh màu
    equalized_b = cv2.equalizeHist(b)
    equalized_g = cv2.equalizeHist(g)
    equalized_r = cv2.equalizeHist(r)

    # Ghép các kênh màu đã cân bằng sáng lại thành ảnh màu
    equalized_image = cv2.merge((equalized_b, equalized_g, equalized_r))
    return equalized_image

image = pre_process(cv2.imread('im1.bmp'))

image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Áp dụng thuật toán Canny để phát hiện cạnh
edges = cv2.Canny(image, threshold1=100, threshold2=200)  # Điều chỉnh ngưỡng tùy ý

# Hiển thị ảnh gốc và ảnh sau khi phát hiện cạnh
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(image, cmap='gray')
plt.title('Ảnh gốc')
plt.subplot(1, 2, 2)
plt.imshow(edges, cmap='gray')
plt.title('Cạnh phát hiện (Canny)')
plt.show()
