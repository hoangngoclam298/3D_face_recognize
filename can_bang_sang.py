import cv2
import numpy as np

def light_balance(image):
    # Chuyển đổi ảnh sang ảnh xám
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Cân bằng lược đồ tần số
    equalized_image = cv2.equalizeHist(gray_image)
    
    # Convert ảnh xám đã cân bằng trở lại ảnh màu
    balanced_image = cv2.cvtColor(equalized_image, cv2.COLOR_GRAY2BGR)
    
    return balanced_image

def bmp_equalization(image):
    # Chuyển đổi ảnh sang ảnh xám
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Bi-histogram equalization
    hist, bins = np.histogram(gray_image.flatten(), 256, [0,256])
    cdf = hist.cumsum()
    cdf_masked = np.ma.masked_equal(cdf, 0)
    cdf_masked = (cdf_masked - cdf_masked.min())*255/(cdf_masked.max()-cdf_masked.min())
    cdf = np.ma.filled(cdf_masked, 0).astype('uint8')
    
    equalized_image = cdf[gray_image]
    
    return equalized_image

def color_balance(image):
    # Chuyển đổi ảnh sang không gian màu LAB
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    
    # Chia các kênh màu
    l, a, b = cv2.split(lab_image)
    
    # Áp dụng cân bằng histogram cho kênh L (độ sáng)
    l_eq = cv2.equalizeHist(l)
    
    # Ghép các kênh màu lại
    balanced_lab_image = cv2.merge((l_eq, a, b))
    
    # Chuyển đổi lại sang không gian màu BGR
    balanced_image = cv2.cvtColor(balanced_lab_image, cv2.COLOR_LAB2BGR)
    
    return balanced_image

def main():
    # Đọc ảnh từ file
    image = cv2.imread(r'test\im0.bmp')
    
    # Áp dụng cân bằng ánh sáng
    balanced_image = light_balance(image)
    
    # Hiển thị ảnh gốc và ảnh đã cân bằng ánh sáng
    cv2.imshow('Original Image', image)
    cv2.imshow('Balanced Image', balanced_image)
    equalized_image = bmp_equalization(image)
    cv2.imshow('Equalized Image', equalized_image)
    balanced_cimage = color_balance(image)
    cv2.imshow('Balanced Image', balanced_cimage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
