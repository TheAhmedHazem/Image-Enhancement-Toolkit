import streamlit as st
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import io

# Import utility functions
from utils import (
    convert_to_grayscale,
    apply_gaussian_blur,
    detect_edges,
    apply_threshold,
    adjust_brightness_contrast,
    apply_watershed_segmentation,
    apply_adaptive_threshold,
    get_pil_image,
    get_downloadable_image
)

# Set page configuration
st.set_page_config(
    page_title="Image Processor",
    page_icon="🖼️",
    layout="wide"
)

# Title and description
st.title("Image Processing App")
st.markdown("Upload an image and apply various processing techniques.")

# Sidebar for controls
st.sidebar.header("Image Processing Controls")

# Upload image widget
uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Main processing function
def process_image(image, operation_type, params=None):
    img_array = np.array(image)
    
    if operation_type == "grayscale":
        return convert_to_grayscale(img_array)
    
    elif operation_type == "blur":
        kernel_size = params.get("kernel_size", 5)
        return apply_gaussian_blur(img_array, kernel_size)
    
    elif operation_type == "edges":
        threshold1 = params.get("threshold1", 100)
        threshold2 = params.get("threshold2", 200)
        return detect_edges(img_array, threshold1, threshold2)
    
    elif operation_type == "threshold":
        thresh_value = params.get("thresh_value", 127)
        return apply_threshold(img_array, thresh_value)
    
    elif operation_type == "color_adjust":
        brightness = params.get("brightness", 0)
        contrast = params.get("contrast", 1)
        return adjust_brightness_contrast(img_array, brightness, contrast)
    
    elif operation_type == "watershed_segmentation":
        return apply_watershed_segmentation(img_array)
        
    elif operation_type == "adaptive_threshold_segmentation":
        block_size = params.get("block_size", 11)
        c_value = params.get("c_value", 2)
        return apply_adaptive_threshold(img_array, block_size, c_value)
    
    return img_array

# Process image when uploaded
if uploaded_file is not None:
    # Read image
    image = Image.open(uploaded_file)
    
    # Display original image
    st.subheader("Original Image")
    st.image(image, caption="Original Image", use_container_width=True)
    
    # Processing options
    operation = st.sidebar.selectbox(
        "Select Operation", 
        ["Original", "Grayscale", "Blur", "Edge Detection", "Threshold", "Color Adjustment", 
         "Watershed Segmentation", "Adaptive Threshold Segmentation"]
    )
    
    # Parameters for different operations
    params = {}
    
    if operation == "Blur":
        params["kernel_size"] = st.sidebar.slider("Blur Amount", 1, 31, 5, step=2)
    
    elif operation == "Edge Detection":
        params["threshold1"] = st.sidebar.slider("Threshold 1", 0, 300, 100)
        params["threshold2"] = st.sidebar.slider("Threshold 2", 0, 300, 200)
    
    elif operation == "Threshold":
        params["thresh_value"] = st.sidebar.slider("Threshold Value", 0, 255, 127)
    
    elif operation == "Color Adjustment":
        params["brightness"] = st.sidebar.slider("Brightness", -100, 100, 0)
        params["contrast"] = st.sidebar.slider("Contrast", 0.0, 3.0, 1.0, 0.1)
    
    elif operation == "Adaptive Threshold Segmentation":
        params["block_size"] = st.sidebar.slider("Block Size (odd)", 3, 51, 11, step=2)
        params["c_value"] = st.sidebar.slider("C Value", -10, 10, 2)
    
    # Process and display the image
    if operation != "Original":
        operation_map = {
            "Grayscale": "grayscale",
            "Blur": "blur",
            "Edge Detection": "edges",
            "Threshold": "threshold",
            "Color Adjustment": "color_adjust",
            "Watershed Segmentation": "watershed_segmentation",
            "Adaptive Threshold Segmentation": "adaptive_threshold_segmentation"
        }
        
        processed_image = process_image(image, operation_map[operation], params)
        st.subheader(f"Processed Image: {operation}")
        st.image(processed_image, caption=f"Processed with {operation}", use_container_width=True)
    
    # Add download button for processed image
    if operation != "Original":
        # Convert the processed image to bytes for download
        if isinstance(processed_image, np.ndarray):
            pil_img = get_pil_image(processed_image)
            byte_img = get_downloadable_image(pil_img)
            
            st.download_button(
                label="Download Processed Image",
                data=byte_img,
                file_name=f"processed_{operation.lower().replace(' ', '_')}.png",
                mime="image/png",
            )

else:
    st.info("Please upload an image to begin processing.")

# Display app information at the bottom
st.sidebar.markdown("---")
st.sidebar.subheader("About")
st.sidebar.info(
    "This app demonstrates various image processing techniques using OpenCV and Streamlit. "
    "Upload an image and experiment with different filters and transformations."
)