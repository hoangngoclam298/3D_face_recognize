import cv2
import numpy as np
import matplotlib.pyplot as plt

# Đọc ảnh
# def pre_process(image):
#     image = cv2.GaussianBlur(image, (5, 5), 0)

#     # Tách các kênh màu
#     b, g, r = cv2.split(image)

#     # Cân bằng sáng cho từng kênh màu
#     equalized_b = cv2.equalizeHist(b)
#     equalized_g = cv2.equalizeHist(g)
#     equalized_r = cv2.equalizeHist(r)

#     # Ghép các kênh màu đã cân bằng sáng lại thành ảnh màu
#     equalized_image = cv2.merge((equalized_b, equalized_g, equalized_r))
#     equalized_image = cv2.GaussianBlur(equalized_image, (5, 5), 0)
#     return equalized_image

def pre_process(image):
    # Chuyển đổi sang không gian màu HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Lấy các kênh màu
    h, s, v = cv2.split(hsv_image)

    # Đặt kênh v thành 1
    v = np.ones_like(v) * 255

    # Ghép lại các kênh màu để tạo ảnh mới
    new_hsv_image = cv2.merge([h, s, v])

    # Chuyển đổi lại sang không gian màu BGR
    final_image = cv2.cvtColor(new_hsv_image, cv2.COLOR_HSV2BGR)
    return s

import os
path_folder = r'Photoface_dist\PhotofaceDB\1001\2008-02-23_12-21-31'
list_image = os.listdir(path_folder)
list_image = [x for x in list_image if x.endswith(".bmp")]
list_image = [pre_process(cv2.imread(os.path.join(path_folder, x))) for x in list_image]

for image in list_image:


# image = pre_process(cv2.imread(r'Photoface_dist\PhotofaceDB\1001\2008-02-23_12-21-31\im2.bmp'))

# image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Áp dụng thuật toán Canny để phát hiện cạnh
    edges = cv2.Canny(image, threshold1=150, threshold2=250)  # Điều chỉnh ngưỡng tùy ý
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
