import streamlit as st
import numpy as np
import cv2
from PIL import Image
import io
from utils.image_processing import process_image
from utils.utils import pil_to_bytes, bytes_to_pil

# Configure page to hide the default navigation
st.set_page_config(
    page_title="Edit Image",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide default Streamlit file navigation with CSS
st.markdown("""
<style>
    .stApp [data-testid="stSidebarNav"] {display: none;}
</style>
""", unsafe_allow_html=True)

# Custom sidebar navigation - fixed paths for Streamlit
st.sidebar.title("Navigation")
if st.sidebar.button("🏠 Home", key="nav_home"):
    st.switch_page("app.py")
if st.sidebar.button("🖼️ Edit Image", key="nav_edit"):
    st.switch_page("pages/edit.py")
if st.sidebar.button("✂️ Crop Image", key="nav_crop"):
    st.switch_page("pages/crop.py")
if st.sidebar.button("🧹 Remove Background", key="nav_bg"):
    st.switch_page("pages/remove_bg.py")
st.sidebar.markdown("---")
st.sidebar.markdown("**Version 2.0** · [GitHub Repo](#)")

st.title("🖼️ Image Editor")

# Add a "Clear Image" button to reset the uploaded image
if st.button("🗑️ Clear Image", key="btn_clear"):
    st.session_state.image_bytes = None
    st.experimental_set_query_params(refresh="true")

if st.session_state.image_bytes is None:
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.session_state.image_bytes = pil_to_bytes(image)
        st.experimental_set_query_params(refresh="true")
else:
    image = bytes_to_pil(st.session_state.image_bytes)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("✂️ Go to Cropping", key="btn_goto_crop"):
        st.switch_page("pages/crop.py")
with col2:
    if st.button("🧹 Remove Background", key="btn_goto_bg"):
        st.switch_page("pages/remove_bg.py")
with col3:
    if st.button("🔄 Reset Edits", key="btn_reset"):
        st.session_state.image_bytes = pil_to_bytes(image)
        st.experimental_set_query_params(refresh="true")

# File uploader at the top
if st.session_state.image_bytes is not None:
    img_array = np.array(image)
    
    # Operation selection
    operation = st.selectbox(
        "Select Operation", 
        ["Grayscale", "Blur", "Edge Detection", "Threshold", "Color Adjustment", 
         "Adaptive Threshold Segmentation", "Watershed Segmentation"],
        index=0
    )
    
    # Parameters in expandable section
    with st.expander("Adjustment Parameters", expanded=True):
        params = {}
        if operation == "Blur":
            params["kernel_size"] = st.slider(
                "Blur Amount", 1, 31, 5, step=2,
                help="Higher values create more blur"
            )
        elif operation == "Edge Detection":
            col1, col2 = st.columns(2)
            with col1:
                params["threshold1"] = st.slider(
                    "Threshold 1", 0, 300, 100,
                    help="First threshold for the hysteresis procedure"
                )
            with col2:
                params["threshold2"] = st.slider(
                    "Threshold 2", 0, 300, 200,
                    help="Second threshold for the hysteresis procedure"
                )
        elif operation == "Threshold":
            params["thresh_value"] = st.slider(
                "Threshold Value", 0, 255, 127,
                help="Pixel values above this will be white, below will be black"
            )
        elif operation == "Color Adjustment":
            col1, col2 = st.columns(2)
            with col1:
                params["brightness"] = st.slider(
                    "Brightness", -100, 100, 0,
                    help="Adjust image brightness"
                )
            with col2:
                params["contrast"] = st.slider(
                    "Contrast", 0.0, 3.0, 1.0, 0.1,
                    help="Adjust image contrast"
                )
        elif operation == "Adaptive Threshold Segmentation":
            col1, col2 = st.columns(2)
            with col1:
                params["block_size"] = st.slider(
                    "Block Size (odd)", 3, 51, 11, step=2,
                    help="Size of pixel neighborhood used for threshold calculation"
                )
            with col2:
                params["c_value"] = st.slider(
                    "C Value", -10, 10, 2,
                    help="Constant subtracted from mean, smaller values give more white areas"
                )
    
    # Process image
    operation_map = {
        "Grayscale": "grayscale",
        "Blur": "blur",
        "Edge Detection": "edges",
        "Threshold": "threshold",
        "Color Adjustment": "color_adjust",
        "Adaptive Threshold Segmentation": "adaptive_threshold_segmentation",
        "Watershed Segmentation": "watershed_segmentation"
    }
    
    processed_image = process_image(img_array, operation_map[operation], params)
    
    # Display images side by side
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original Image")
        st.image(image)
    
    with col2:
        st.subheader("Processed Image")
        st.image(processed_image)
    
    # Download button
    if isinstance(processed_image, np.ndarray):
        if len(processed_image.shape) == 2:
            pil_img = Image.fromarray(processed_image)
        else:
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
    st.info("Please upload an image to begin editing.")