import streamlit as st
from PIL import Image
import io
from utils.utils import pil_to_bytes, bytes_to_pil

# Configure page to hide the default navigation
st.set_page_config(
    page_title="Image Cropper",
    page_icon="✂️",
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

st.title("✂️ Image Cropper")

# Upload image section
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Use either the uploaded image or the one from session state
if uploaded_file is not None:
    # Use the newly uploaded image
    image = Image.open(uploaded_file)
    # Store in session state for other pages
    st.session_state.image_bytes = pil_to_bytes(image)
elif st.session_state.get('image_bytes') is not None:
    # Use the image from session state if available
    image = bytes_to_pil(st.session_state.image_bytes)
else:
    # No image available
    st.info("Please upload an image to begin cropping.")
    st.stop()

# Get image dimensions
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
