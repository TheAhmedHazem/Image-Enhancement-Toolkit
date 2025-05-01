import streamlit as st
from PIL import Image
import io
from utils.utils import pil_to_bytes, bytes_to_pil

# Initialize session state
if 'image_bytes' not in st.session_state:
    st.session_state.image_bytes = None

# Sidebar navigation

st.sidebar.page_link("app.py", label="🏠 Home")
st.sidebar.page_link("pages/edit.py", label="🖼️ Edit Image")
st.sidebar.page_link("pages/crop.py", label="✂️ Crop Image")
st.sidebar.page_link("pages/remove_bg.py", label="🧹 Remove Background")
st.sidebar.markdown("---")
st.sidebar.markdown("**Version 2.0** · [GitHub Repo](#)")