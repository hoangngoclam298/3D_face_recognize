import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

def merge_image(list_image):
    image1, image2, image3, image4 = tuple(list_image)
    if image1.shape == image2.shape == image3.shape == image4.shape:
        blended_image = cv2.addWeighted(image1, 0.25, image2, 0.25, 0)
        blended_image = cv2.addWeighted(blended_image, 0.5, image3, 0.25, 0)
        blended_image = cv2.addWeighted(blended_image, 0.5, image4, 0.25, 0)
        return cv2.cvtColor(blended_image, cv2.COLOR_BGR2GRAY)

def adjust_gamma(image, gamma=1.0):
    # Build a lookup table mapping the pixel values [0, 255] to their adjusted gamma values
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    
    # Apply gamma correction using the lookup table
    return cv2.LUT(image, table)

path_folder = r'Photoface_dist\PhotofaceDB\1001\2008-02-23_12-21-31'

list_name_image = [x for x in os.listdir(path_folder) if x.endswith(".bmp")]

list_image = [cv2.imread(os.path.join(path_folder, x)) for x in list_name_image]

merge_result = merge_image(list_image)

edges = cv2.Canny(merge_result, threshold1=50, threshold2=150)# Điều chỉnh ngưỡng tùy ý
print(edges[20:-20,20:-20].shape)

# Hiển thị ảnh gốc và ảnh sau khi phát hiện cạnh
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(merge_result, cmap='gray')
plt.title('Ảnh gốc')
plt.subplot(1, 2, 2)
plt.imshow(edges, cmap='gray')
plt.title('Cạnh phát hiện (Canny)')
plt.show()

# cv2.imshow("merge image", merge_result)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

