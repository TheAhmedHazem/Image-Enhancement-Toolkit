import streamlit as st
from PIL import Image
import io
from utils.utils import pil_to_bytes, bytes_to_pil

st.title("✂️ Image Cropper")

if st.session_state.image_bytes is None:
    st.error("No image found. Please upload an image in the Edit page.")
    st.stop()
else:
    image = bytes_to_pil(st.session_state.image_bytes)


uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    width, height = image.size
    
    # Crop controls in expandable section
    with st.expander("Crop Settings", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            left = st.slider("Left", 0, width-1, 0)
            right = st.slider("Right", left+1, width, width)
        with col2:
            top = st.slider("Top", 0, height-1, 0)
            bottom = st.slider("Bottom", top+1, height, height)
    
    # Perform cropping
    cropped_image = image.crop((left, top, right, bottom))
    
    # Display images side by side
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original Image")
        st.image(image, use_column_width=True)
    
    with col2:
        st.subheader("Cropped Image")
        st.image(cropped_image, use_column_width=True)
    
    # Download button
    buf = io.BytesIO()
    cropped_image.save(buf, format="PNG")
    st.session_state.image_bytes = pil_to_bytes(cropped_image)
    byte_img = buf.getvalue()
    
    st.download_button(
        label="Download Cropped Image",
        data=byte_img,
        file_name="cropped_image.png",
        mime="image/png",
    )
else:
    st.info("Please upload an image to begin cropping.")
