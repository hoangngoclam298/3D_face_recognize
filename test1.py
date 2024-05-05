import cv2
import numpy as np

def random_flip(image, probability=0.5):
    """
    Thực hiện phép đảo ngẫu nhiên trên hình ảnh.

    Args:
    - image: Hình ảnh gốc.
    - probability: Xác suất của phép đảo (mặc định là 0.5).

    Returns:
    - flipped_image: Hình ảnh sau khi đã được đảo (nếu có).
    """
    if np.random.rand() < probability:
        flipped_image = cv2.flip(image, np.random.randint(-1, 2))  # -1: ngẫu nhiên, 0: dọc, 1: ngang
        return flipped_image
    return image

def random_rotation(image, max_angle=15):
    """
    Thực hiện phép quay ngẫu nhiên trên hình ảnh.

    Args:
    - image: Hình ảnh gốc.
    - max_angle: Góc quay tối đa (đơn vị: độ, mặc định là 30).

    Returns:
    - rotated_image: Hình ảnh sau khi đã được quay.
    """
    angle = np.random.uniform(-max_angle, max_angle)
    height, width = image.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height), borderMode=cv2.BORDER_REFLECT)
    return rotated_image

def random_contrast(image, lower=0.5, upper=1.5):
    """
    Thực hiện phép tăng cường độ tương phản ngẫu nhiên trên hình ảnh.

    Args:
    - image: Hình ảnh gốc.
    - lower: Giá trị tối thiểu của độ tương phản (mặc định là 0.5).
    - upper: Giá trị tối đa của độ tương phản (mặc định là 1.5).

    Returns:
    - contrasted_image: Hình ảnh sau khi đã được tăng cường độ tương phản.
    """
    contrast_factor = np.random.uniform(lower, upper)
    mean_intensity = np.mean(image)
    contrasted_image = (image - mean_intensity) * contrast_factor + mean_intensity
    return np.clip(contrasted_image, 0, 255).astype(np.uint8)

# Load hình ảnh
image = cv2.imread('merge_image.png')

# Áp dụng phép đảo ngẫu nhiên
flipped_image = random_flip(image)

# Áp dụng phép quay ngẫu nhiên
rotated_image = random_rotation(image)

# Áp dụng phép tăng cường độ tương phản ngẫu nhiên
contrasted_image = random_contrast(image)

# Hiển thị hình ảnh gốc và hình ảnh sau khi áp dụng phép đảo và phép quay
cv2.imshow('Original Image', image)
cv2.imshow('Random Flipped Image', flipped_image)
cv2.imshow('Random Rotated Image', rotated_image)
cv2.imshow('Random Contrasted Image', contrasted_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
