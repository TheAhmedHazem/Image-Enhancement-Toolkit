import cv2
import numpy as np
from PIL import Image
import io

def convert_to_grayscale(image_array):
    """Convert an RGB image to grayscale."""
    return cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)

def apply_gaussian_blur(image_array, kernel_size=5):
    """Apply Gaussian blur to an image."""
    return cv2.GaussianBlur(image_array, (kernel_size, kernel_size), 0)

def detect_edges(image_array, threshold1=100, threshold2=200):
    """Detect edges in an image using Canny edge detection."""
    gray = convert_to_grayscale(image_array)
    return cv2.Canny(gray, threshold1, threshold2)

def apply_threshold(image_array, thresh_value=127):
    """Apply binary thresholding to an image."""
    gray = convert_to_grayscale(image_array)
    _, binary = cv2.threshold(gray, thresh_value, 255, cv2.THRESH_BINARY)
    return binary

def adjust_brightness_contrast(image_array, brightness=0, contrast=1.0):
    """Adjust brightness and contrast of an image."""
    return cv2.convertScaleAbs(image_array, alpha=contrast, beta=brightness)

def apply_watershed_segmentation(image_array):
    """Apply watershed segmentation to an image."""
    # Convert to grayscale and blur
    gray = convert_to_grayscale(image_array)
    blur = apply_gaussian_blur(gray)
    
    # Apply Otsu's thresholding
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Noise removal with morphological operations
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    
    # Sure background area
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    
    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)
    
    # Finding unknown region
    unknown = cv2.subtract(sure_bg, sure_fg)
    
    # Marker labelling
    _, markers = cv2.connectedComponents(sure_fg)
    markers += 1  # Add one to all labels so that background is 1, not 0
    markers[unknown == 255] = 0  # Mark the unknown region with 0
    
    # Apply watershed
    markers = cv2.watershed(image_array.copy(), markers)
    
    # Create a color visualization of the markers
    result = image_array.copy()
    result[markers == -1] = [0, 0, 255]  # Mark boundaries in red
    
    return result

def apply_adaptive_threshold(image_array, block_size=11, c_value=2):
    """Apply adaptive thresholding to an image."""
    gray = convert_to_grayscale(image_array)
    adaptive_thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, block_size, c_value
    )
    return cv2.cvtColor(adaptive_thresh, cv2.COLOR_GRAY2RGB)

def get_pil_image(numpy_image):
    """Convert numpy array to PIL Image."""
    if len(numpy_image.shape) == 2:  # Grayscale
        return Image.fromarray(numpy_image)
    else:  # Color
        return Image.fromarray(numpy_image)

def get_downloadable_image(pil_image):
    """Convert PIL image to bytes for download."""
    buf = io.BytesIO()
    pil_image.save(buf, format="PNG")
    return buf.getvalue()