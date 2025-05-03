import streamlit as st
from PIL import Image
import io
from utils.utils import pil_to_bytes, bytes_to_pil
def crop_page():
    st.title("✂️ Image Cropper")

    # Check if an image is available in session state
    if st.session_state.image_bytes is None:
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            # Save the uploaded image to session state
            image = Image.open(uploaded_file)
            st.session_state.image_bytes = pil_to_bytes(image)
        else:
            st.stop()
    else:
        # Retrieve the image from session state
        image = bytes_to_pil(st.session_state.image_bytes)

    # Get image dimensions
    width, height = image.size

    # Crop controls in expandable section
    with st.expander("Crop Settings", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            left = st.slider("Left", 0, width - 1, 0)
            right = st.slider("Right", left + 1, width, width)
        with col2:
            top = st.slider("Top", 0, height - 1, 0)
            bottom = st.slider("Bottom", top + 1, height, height)

    # Perform cropping
    cropped_image = image.crop((left, top, right, bottom))

    # Display images side by side
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original Image")
        st.image(image)

    with col2:
        st.subheader("Cropped Image")
        st.image(cropped_image)

    # Add a "Confirm Crop" button
    if st.button("Confirm Crop"):
        # Save the cropped image back to session state
        st.session_state.image_bytes = pil_to_bytes(cropped_image)
        st.success("Cropped image saved successfully!")

    # Download button for the cropped image
    buf = io.BytesIO()
    cropped_image.save(buf, format="PNG")
    byte_img = buf.getvalue()

    st.download_button(
        label="Download Cropped Image",
        data=byte_img,
        file_name="cropped_image.png",
        mime="image/png",
    )