import streamlit as st
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import os
import io

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
        
        # Apply brightness and contrast adjustment
        adjusted = cv2.convertScaleAbs(img_array, alpha=contrast, beta=brightness)
        return adjusted
    
    return img_array

# Process image when uploaded
if uploaded_file is not None:
    # Read image
    image = Image.open(uploaded_file)
    
    # Display original image
    st.subheader("Original Image")
    st.image(image, caption="Original Image", use_column_width=True)
    
    # Processing options
    operation = st.sidebar.selectbox(
        "Select Operation", 
        ["Original", "Grayscale", "Blur", "Edge Detection", "Threshold", "Color Adjustment"]
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
    
    # Process and display the image
    if operation != "Original":
        operation_map = {
            "Grayscale": "grayscale",
            "Blur": "blur",
            "Edge Detection": "edges",
            "Threshold": "threshold",
            "Color Adjustment": "color_adjust"
        }
        
        processed_image = process_image(image, operation_map[operation], params)
        st.subheader(f"Processed Image: {operation}")
        st.image(processed_image, caption=f"Processed with {operation}", use_column_width=True)
    
    # Add download button for processed image
    if operation != "Original":
        # Convert the processed image to bytes for download
        if isinstance(processed_image, np.ndarray):
            # Convert numpy array to PIL Image
            if len(processed_image.shape) == 2:  # Grayscale
                pil_img = Image.fromarray(processed_image)
            else:  # Color
                pil_img = Image.fromarray(processed_image)
                
            buf = io.BytesIO()
            pil_img.save(buf, format="PNG")
            byte_img = buf.getvalue()
            
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