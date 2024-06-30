import cv2
import matplotlib.pyplot as plt

# Đường dẫn tới các ảnh
image_paths = [
    r'Photoface_dist\PhotofaceDB\1001\2008-03-01_07-57-06\im0.bmp',
    r'Photoface_dist\PhotofaceDB\1001\2008-03-01_07-57-06\im1.bmp',
    r'Photoface_dist\PhotofaceDB\1001\2008-03-01_07-57-06\im2.bmp',
    r'Photoface_dist\PhotofaceDB\1001\2008-03-01_07-57-06\im3.bmp'
]

# Đọc ảnh sử dụng OpenCV
images = [cv2.imread(image_path) for image_path in image_paths]

# Chuyển đổi ảnh từ BGR (OpenCV) sang RGB (matplotlib)
# images_rgb = [cv2.cvtColor(image, cv2.COLOR_BGR2RGB) for image in images]

top_row = cv2.hconcat([images[2], images[1]])
# Ghép ảnh 3 và 4 theo chiều ngang
bottom_row = cv2.hconcat([images[3], images[0]])
# Ghép hai hàng ảnh lại với nhau theo chiều dọc
grid_image = cv2.vconcat([top_row, bottom_row])

# Hiển thị ảnh đã ghép
cv2.imshow('Grid Image', grid_image)
cv2.imwrite('test_4img.png', grid_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
