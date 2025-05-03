import streamlit as st
from PIL import Image
import io
from utils.utils import pil_to_bytes, bytes_to_pil

# Initialize session state
if 'image_bytes' not in st.session_state:
    st.session_state.image_bytes = None

# Configure page to hide the default navigation
st.set_page_config(
    page_title="Image Enhancement Toolkit",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Hide default Streamlit file navigation with CSS
st.markdown("""
<style>
    .stApp [data-testid="stSidebarNav"] {display: none;}
    /* This hides the default file navigation but keeps your custom navigation below */
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

# Main page content
st.title("Image Enhancement Toolkit")

# Introduction text
st.markdown("""
### Welcome to the Image Enhancement Toolkit!

This application provides a suite of powerful tools to enhance and manipulate your images:
""")

# Feature columns
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🖼️ Edit")
    st.markdown("Apply filters, adjust colors, detect edges, and more.")
    
with col2:
    st.markdown("### ✂️ Crop")
    st.markdown("Precisely trim your images to the perfect dimensions.")
    
with col3:
    st.markdown("### 🧹 Remove Background")
    st.markdown("Extract subjects from backgrounds with one click.")

# Central image area
st.markdown("---")

# Center column for the image
left_spacer, center_col, right_spacer = st.columns([1, 3, 1])

with center_col:
    # Upload button to get started
    uploaded_file = st.file_uploader("Upload an image to get started", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Store in session state for other pages
        st.session_state.image_bytes = pil_to_bytes(image)
        
        # Quick action buttons
        st.markdown("### Quick Actions")
        action_col1, action_col2, action_col3 = st.columns(3)
        
        with action_col1:
            if st.button("Edit Image", key="btn_goto_edit"):
                st.switch_page("pages/edit.py")
        
        with action_col2:
            if st.button("Crop Image", key="btn_goto_crop"):
                st.switch_page("pages/crop.py")
        
        with action_col3:
            if st.button("Remove Background", key="btn_goto_bg"):
                st.switch_page("pages/remove_bg.py")
    else:
        # Placeholder when no image is uploaded
        st.info("👆 Upload an image or navigate to any tool using the sidebar.")

# Footer
st.markdown("---")
st.markdown("#### About")
st.markdown("""
This toolkit uses advanced image processing techniques to help you enhance your images.
Powered by OpenCV, PIL, and other libraries.
""")