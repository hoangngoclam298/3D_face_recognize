import cv2

# Load ảnh chính và ảnh phụ
image1 = cv2.imread('im0.bmp')
image2 = cv2.imread('im3.bmp')

if image1.shape != image2.shape:
    print("Kích thước của hai ảnh không giống nhau.")
    exit()

# Tạo một hình ảnh mới để lồng hai ảnh vào đó
merged_image = cv2.addWeighted(image1, 0.5, image2, 0.5, 0)

merged_image = cv2.hconcat([image1, image2, merged_image])

cv2.imshow('Merged Image', merged_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
