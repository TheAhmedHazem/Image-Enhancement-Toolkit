import streamlit as st
from PIL import Image
from rembg import remove
import io
import numpy as np
from utils.utils import pil_to_bytes, bytes_to_pil

def remove_background(image):
    """Wrapper for your existing bg removal function"""
    transparent = remove(image)
    return image, transparent

st.title("🧹 Background Remover")

if st.session_state.image_bytes is None:
    st.error("No image found. Please upload an image in the Edit page.")
    st.stop()
else:
    image = bytes_to_pil(st.session_state.image_bytes)


# Custom CSS for better layout
st.markdown("""
<style>
    .image-container {
        display: flex;
        justify-content: space-between;
        margin-bottom: 2rem;
    }
    .image-box {
        width: 48%;
        text-align: center;
        padding: 1rem;
        border-radius: 8px;
        background: #1e1e1e;
    }
    .stDownloadButton button {
        width: 100%;
        margin-top: 1rem;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Process image
    original = Image.open(uploaded_file)
    original, transparent = remove_background(original)
    
    # Display side by side
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Image")
        st.image(original)
    
    with col2:
        st.subheader("Background Removed")
        st.image(transparent)
    
    # Download buttons
    col1, col2 = st.columns(2)
    
    with col1:
        # Original download
        buf_original = io.BytesIO()
        original.save(buf_original, format="PNG")
        st.download_button(
            label="⬇️ Download Original",
            data=buf_original.getvalue(),
            file_name="original.png",
            mime="image/png"
        )
    
    with col2:
        # Transparent download
        buf_transparent = io.BytesIO()
        
        transparent.save(buf_transparent, format="PNG")
        st.download_button(
            label="⬇️ Download Transparent",
            data=buf_transparent.getvalue(),
            file_name="transparent.png",
            mime="image/png"
        )
        st.session_state.image_bytes = pil_to_bytes(transparent)

    
    # Additional options
    with st.expander("⚙️ Advanced Options"):
        # Background color preview
        bg_color = st.color_picker("Preview with background color", "#FFFFFF")
        
        # Create preview with selected background
        if transparent.mode == 'RGBA':
            background = Image.new('RGBA', transparent.size, bg_color)
            preview = Image.alpha_composite(background, transparent)
            st.image(preview, caption=f"Preview on {bg_color} background")
            
            # Download preview
            buf_preview = io.BytesIO()
            preview.save(buf_preview, format="PNG")
            st.download_button(
                label="⬇️ Download with Background",
                data=buf_preview.getvalue(),
                file_name=f"preview_{bg_color}.png",
                mime="image/png"
            )
else:
    st.info("Please upload an image to remove the background")

# Add to sidebar navigation in app.py