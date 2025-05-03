import streamlit as st
from PIL import Image
import io
from utils.utils import pil_to_bytes, bytes_to_pil
from rembg import remove
from utils.image_processing import process_image
from sections.crop import crop_page
from sections.remove_bg import remove_bg_page
from sections.edit import edit_page

import numpy as np 
import cv2 
import os 
import base64 

# Initialize session state
if 'image_bytes' not in st.session_state:
    st.session_state.image_bytes = None

# Initialize session state for navigation
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

def get_logo(logo_path="Image-Enhancement-Toolkit\\static\\ggg.jpg", size=(110, 110)): 
    if os.path.exists(logo_path): 
        img = Image.open(logo_path) 
        img = img.resize(size, Image.LANCZOS) 
        buffered = io.BytesIO() 
        img.save(buffered, format="PNG") 
        return base64.b64encode(buffered.getvalue()).decode() 
    return "" 

# Get the logo
logo_base64 = get_logo(size=(110, 110))

# Set page config
st.set_page_config(
    page_title="Pixel Perfect Processor",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
# CSS with your color scheme 
st.markdown(f""" 
<style> 
:root {{ 
    --primary: #121212; 
    --secondary: #1E1E1E; 
    --accent1: #B44CFF; 
    --accent2: #00CFFF; 
    --text: #FFFFFF; 
}} 
 
.stApp {{ 
    background-color: var(--primary); 
    color: var(--text); 
}} 
 
.logo-container {{ 
    text-align: center; 
    margin-bottom: 20px; 
}} 
 
.logo-img {{ 
    max-width: 150px; 
    height: auto; 
}}
.description {{ 
    background-color: var(--secondary); 
    padding: 20px; 
    border-radius: 10px; 
    margin: 20px 0; 
    border-left: 4px solid var(--accent1); 
}} 
 
.feature-card {{ 
    background-color: var(--secondary); 
    padding: 15px; 
    border-radius: 10px; 
    margin-bottom: 15px; 
    border-left: 4px solid var(--accent2); 
}} 
 
.feature-title {{ 
    color: var(--accent1); 
    font-weight: bold; 
}} 
 
.team-section {{ 
    background-color: var(--secondary); 
    padding: 20px; 
    border-radius: 10px; 
    text-align: center; 
    margin-top: 30px; 
}} 
 
h1, h2, h3 {{ 
    color: #FFFFF !important; 
}}

sidebar .sidebar-content {{
    background-color: var(--accent1);
    color: var(--text);
}} 
</style> 
""", unsafe_allow_html=True) 

def home_page(): 
    # Display only one centered logo (150px) 
    if logo_base64: 
        st.markdown(f""" 
        <div class="logo-container"> 
            <img class="logo-img" src="data:image/png;base64,{logo_base64}"> 
        </div> 
        """, unsafe_allow_html=True) 
    else: 
        st.markdown(""" 
        <div class="logo-container"> 
            <h2 style="color: var(--accent2)">PIXEL PERFECT</h2> 
        </div> 
        """, unsafe_allow_html=True) 
 
    # Brief about image enhancement 
    st.markdown(""" 
    <div class="description"> 
        <h2 style="text-align: center;">Welcome to <span style="color: var(--accent1)">Pixel Perfect</span> Processor</h2> 
        <p>Image enhancement transforms ordinary photos into professional-quality visuals. <p>In our digital age, images have become more than just pictures - they're powerful communication tools that shape our daily lives:</p> 
        <p><b>💼 Professional Impact:</b> Job seekers with professional profile pictures receive 21x more profile views and 9x more connection requests.</p> 
        <p><b>🧠 Memory & Learning:</b> People remember 80% of what they see, compared to just 20% of what they read, making visuals crucial for education.</p> 
        <p><b>🚀 Brand Perception:</b> Consistent, high-quality visuals across platforms can increase revenue by up to 23% through improved brand recognition.</p> 
        <p>Our processor helps you create images that make an impact - whether for personal memories, professional portfolios, or business marketing.</p> 
    </div> 
    """, unsafe_allow_html=True) 
# Features section 
    st.markdown(""" 
    <h2 style="text-align: center;">Professional-Grade Features</h2> 
 
    <div class="feature-card"> 
        <div class="feature-title">Background Removal</div> 
        <p>Automatically isolate subjects with clean, precise cutouts for professional compositions.</p> 
    </div> 
 
    <div class="feature-card"> 
        <div class="feature-title">Precision Cropping</div> 
        <p>Smart cropping tools with composition guides for perfect framing every time.</p> 
    </div> 
 
    <div class="feature-card"> 
        <div class="feature-title">Color Enhancement</div> 
        <p>Advanced color correction to make your images vibrant and true-to-life.</p> 
    </div> 
 
    <div class="feature-card"> 
        <div class="feature-title">Professional Blur Effects</div> 
        <p>Create beautiful depth-of-field effects to highlight your subjects.</p> 
    </div> 
 
    <div class="feature-card"> 
        <div class="feature-title">Edge Detection</div> 
        <p>Precision tools for technical analysis and creative edge effects.</p> 
    </div> 
    """, unsafe_allow_html=True) 
# Team section 
    st.markdown(""" 
    <div class="team-section"> 
        <div style="color: var(--accent2); font-weight: bold;">Created By</div> 
        <div style="margin: 15px 0;"> 
            Ramez Ezzat • Mariam Sobhy<br> 
            Ahmed Hazem • Noureen 
        </div> 
    </div> 
    """, unsafe_allow_html=True) 

# Sidebar navigation
st.sidebar.title("Navigation")
if st.sidebar.button("🏠 Home", key=1):
    st.session_state.current_page = "home"
if st.sidebar.button("🖼️ Edit Image", key=2):
    st.session_state.current_page = "edit"
if st.sidebar.button("✂️ Crop Image", key=3):
    st.session_state.current_page = "crop"
if st.sidebar.button("🧹 Remove Background", key=4):
    st.session_state.current_page = "remove_bg"

st.sidebar.markdown("---")
st.sidebar.markdown("**Version 2.0** · [GitHub Repo](#)")

# Page routing based on session state
if st.session_state.current_page == "home":
    home_page()
elif st.session_state.current_page == "edit":
    edit_page()
elif st.session_state.current_page == "crop":
    crop_page()
elif st.session_state.current_page == "remove_bg":
    remove_bg_page()
else:
    st.error("Page not found!")
