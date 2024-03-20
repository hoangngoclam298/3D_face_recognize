import cv2

# Đường dẫn của file ảnh
filename = "im0.bmp"
image = cv2.imread(filename)

# Đọc ảnh
def pre_process(image):
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)

    # Tách các kênh màu
    b, g, r = cv2.split(blurred_image)

    # Cân bằng sáng cho từng kênh màu
    equalized_b = cv2.equalizeHist(b)
    equalized_g = cv2.equalizeHist(g)
    equalized_r = cv2.equalizeHist(r)

    # Ghép các kênh màu đã cân bằng sáng lại thành ảnh màu
    equalized_image = cv2.merge((equalized_b, equalized_g, equalized_r))
    return equalized_image

# Hiển thị ảnh gốc và ảnh đã xóa nhiễu và đã cân bằng sáng
cv2.imshow("Original Image", image)
cv2.imshow("Equalized Image", pre_process(image))
cv2.waitKey(0)
cv2.destroyAllWindows()

