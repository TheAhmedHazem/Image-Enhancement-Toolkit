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
    elif operation_type == "log_transform":
        
        c = 255 / np.log(1 + np.max(img_array))
        img_array = c * (np.log(img_array + 1))
        img_array = np.array(np.clip(img_array, 0, 255), dtype=np.uint8)
        return img_array
    elif operation_type == "negative":
        return 255 - img_array
    elif operation_type == "piecewise":
        # Default piecewise mapping: identity (no change)
        r_vals = np.array(params.get("r_vals", [0, 70, 150, 255]), dtype=np.uint8)
        s_vals = np.array(params.get("s_vals", [0, 50, 200, 255]), dtype=np.uint8)

        # Ensure correct shape and clipping
        r_vals = np.clip(r_vals, 0, 255)
        s_vals = np.clip(s_vals, 0, 255)

        # Apply interpolation separately for grayscale or each channel
        if len(img_array.shape) == 2:  # Grayscale
            flat = img_array.flatten()
            mapped = np.interp(flat, r_vals, s_vals)
            result = mapped.reshape(img_array.shape).astype(np.uint8)
        else:  # Color image: apply to each channel
            result = np.zeros_like(img_array)
            for c in range(img_array.shape[2]):
                flat = img_array[:, :, c].flatten()
                mapped = np.interp(flat, r_vals, s_vals)
                result[:, :, c] = mapped.reshape(img_array.shape[:2]).astype(np.uint8)

        return result
    return img_array