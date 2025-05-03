import streamlit as st
from PIL import Image
from rembg import remove
import io
from utils.utils import pil_to_bytes, bytes_to_pil

def remove_bg_page():
    def remove_background(image):
        """Wrapper for your existing bg removal function"""
        transparent = remove(image)
        return transparent

    st.title("🧹 Background Remover")

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

    # Display the original image and preview side by side
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Image")
        st.image(image)

    with col2:
        st.subheader("Preview: Background Removed")
        transparent_preview = remove_background(image)
        st.image(transparent_preview)

    # Add a button to confirm background removal
    if st.button("Confirm Remove Background"):
        # Save the background-removed image back to session state
        st.session_state.image_bytes = pil_to_bytes(transparent_preview)
        st.success("Background removed successfully!")

        # Provide a download button for the modified image
        buf_transparent = io.BytesIO()
        transparent_preview.save(buf_transparent, format="PNG")
        st.download_button(
            label="⬇️ Download Background Removed Image",
            data=buf_transparent.getvalue(),
            file_name="background_removed.png",
            mime="image/png"
        )
    