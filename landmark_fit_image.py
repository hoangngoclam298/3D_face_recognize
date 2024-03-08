import cv2
import numpy as np

def gray_to_3_channels(gray_image):
    # Tạo ba kênh màu giống nhau từ ảnh xám ban đầu
    blue_channel = gray_image.copy()
    green_channel = gray_image.copy()
    red_channel = gray_image.copy()

    # Ghép ba kênh màu lại thành ảnh màu
    merged_image = cv2.merge([blue_channel, green_channel, red_channel])

    return merged_image

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

    return gray_to_3_channels(equalized_image)

# Đọc ảnh gốc và ảnh dịch chuyển
func_balance = bmp_equalization

small_image = func_balance(cv2.imread('im3.bmp'))[80:-80,80:-80,:]
large_image = func_balance(cv2.imread('im3.bmp'))


# Chuyển ảnh sang đen trắng
large_gray = cv2.cvtColor(large_image, cv2.COLOR_BGR2GRAY)
small_gray = cv2.cvtColor(small_image, cv2.COLOR_BGR2GRAY)

# Khởi tạo bộ phát hiện và trích xuất đặc trưng SIFT
sift = cv2.SIFT_create()

# Tìm các điểm đặc trưng và mô tả chúng cho cả hai ảnh
keypoints_large, descriptors_large = sift.detectAndCompute(large_gray, None)
keypoints_small, descriptors_small = sift.detectAndCompute(small_gray, None)

# Khởi tạo matcher và thực hiện matching
bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
matches = bf.match(descriptors_small, descriptors_large)


matched_image = cv2.drawMatches(small_image, keypoints_small, large_image, keypoints_large, matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

# Hiển thị ảnh với các điểm matches
cv2.imshow('Matches', matched_image)
cv2.waitKey(0)
cv2.destroyAllWindows()


# # Tính toán tổng của vectơ dịch chuyển
# total_dx = 0
# total_dy = 0
# for match in matches:
#     total_dx += keypoints_large[match.trainIdx].pt[0] - keypoints_small[match.queryIdx].pt[0]
#     total_dy += keypoints_large[match.trainIdx].pt[1] - keypoints_small[match.queryIdx].pt[1]

# # Tính toán vectơ dịch chuyển trung bình
# mean_dx = total_dx / len(matches)
# mean_dy = total_dy / len(matches)

# # Tính toán khung cần dịch chuyển
# h, w = small_gray.shape
# top_left = (int(mean_dx), int(mean_dy))
# bottom_right = (int(mean_dx) + w, int(mean_dy) + h)

# # Vẽ hộp giới hạn trên ảnh lớn
# cv2.rectangle(large_image, top_left, bottom_right, (0, 255, 0), 2)

# # Hiển thị ảnh lớn với khung ảnh nhỏ được vẽ lên
# cv2.imshow('Bounding Box', large_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()