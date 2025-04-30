import cv2
import numpy as np

def process_image(img_array, operation_type, params=None):
    if operation_type == "grayscale":
        return cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    elif operation_type == "blur":
        kernel_size = params.get("kernel_size", 5)
        return cv2.GaussianBlur(img_array, (kernel_size, kernel_size), 0)
    elif operation_type == "edges":
        threshold1 = params.get("threshold1", 100)
        threshold2 = params.get("threshold2", 200)
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        return cv2.Canny(gray, threshold1, threshold2)
    elif operation_type == "threshold":
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        thresh_value = params.get("thresh_value", 127)
        _, binary = cv2.threshold(gray, thresh_value, 255, cv2.THRESH_BINARY)
        return binary
    elif operation_type == "color_adjust":
        brightness = params.get("brightness", 0)
        contrast = params.get("contrast", 1)
        return cv2.convertScaleAbs(img_array, alpha=contrast, beta=brightness)
    return img_array