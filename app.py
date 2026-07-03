import streamlit as st
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import segno
import base64
import io
import os

# --- 1. GLOBAL WORKSPACE CONFIGURATION ---
st.set_page_config(
    page_title="PixelCraft & QR Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished interface styling
st.markdown("""
    <style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #1E3A8A; margin-bottom: 0.5rem; }
    .sub-header { font-size: 1.1rem; color: #4B5563; margin-bottom: 2rem; }
    .section-block { padding: 1.5rem; border-radius: 0.5rem; background-color: #F3F4F6; margin-bottom: 1rem; }
    .error-text { color: #DC2626; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# --- 2. WORKSPACE NAVIGATION ---
st.sidebar.title("⚡ Workspace Hub")
workspace_mode = st.sidebar.radio(
    "Select Functional Engine:",
    ["🎨 Advanced Image Studio", "🔮 Universal QR Engine"]
)
st.sidebar.markdown("---")

# ==========================================
# MODE A: ADVANCED IMAGE STUDIO
# ==========================================
if workspace_mode == "🎨 Advanced Image Studio":
    st.markdown('<div class="main-header">🎨 Advanced Image Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Manipulate, filter, resize, and optimize images with real-time compression metrics.</div>', unsafe_allow_html=True)

    uploaded_img_file = st.file_uploader("Upload target image layer...", type=["png", "jpg", "jpeg"])

    if uploaded_img_file is not None:
        try:
            # Initialize core image object
            original_image = Image.open(uploaded_img_file)
            img_format = original_image.format if original_image.format else "PNG"
            
            # Workspace Control panel split from presentation grid
            st.sidebar.header("⚙️ Studio Adjustment Panel")
            
            # Filter Controller
            selected_filter = st.sidebar.selectbox(
                "Visual Filter State:",
                ["Original", "Black & White", "Sepia Tone", "Gaussian Blur", "Contour Sketch", "Vibrant Saturation", "Retro Negative", "Emboss Art"]
            )
            
            # Direct Manipulation Canvas Tools
            st.sidebar.markdown("### 📐 Canvas Geometry")
            
            # Resize Tool
            orig_w, orig_h = original_image.size
            maintain_aspect = st.sidebar.checkbox("Maintain Aspect Ratio", value=True)
            
            if maintain_aspect:
                new_width = st.sidebar.number_input("Target Width (px):", min_value=1, max_value=8000, value=orig_w)
                ratio = float(new_width) / float(orig_w)
                new_height = int(orig_h * ratio)
                st.sidebar.caption(f"Calculated Height: {new_height}px")
            else:
                new_width = st.sidebar.number_input("Target Width (px):", min_value=1, max_value=8000, value=orig_w)
                new_height = st.sidebar.number_input("Target Height (px):", min_value=1, max_value=8000, value=orig_h)

            # Crop Tool Boundaries
            st.sidebar.markdown("### ✂️ Boundary Slicing (Margins)")
            crop_left = st.sidebar.slider("Crop Left Margin (px)", 0, orig_w // 2, 0)
            crop_right = st.sidebar.slider("Crop Right Margin (px)", 0, orig_w // 2, 0)
            crop_top = st.sidebar.slider("Crop Top Margin (px)", 0, orig_h // 2, 0)
            crop_bottom = st.sidebar.slider("Crop Bottom Margin (px)", 0, orig_h // 2, 0)
            
            # Compression Optimization Setup
            st.sidebar.markdown("### 📉 Compression Engine")
            compression_quality = st.sidebar.slider("Export Quality Target:", 1, 100, 85)

            # --- PROCESSING ENGINE PIPELINE WITH CONTAINMENT SHIELD ---
            with st.spinner("Processing image matrix transformation..."):
                try:
                    # Step 1: Clone reference
                    working_img = original_image.copy()
                    
                    # Step 2: Crop Manipulation
                    if crop_left + crop_right < orig_w and crop_top + crop_bottom < orig_h:
                        crop_box = (crop_left, crop_top, orig_w - crop_right, orig_h - crop_bottom)
                        working_img = working_img.crop(crop_box)
                    else:
                        st.warning("⚠️ Invalid cropping bounds. Slice logic bypassed.")

                    # Step 3: Resize Execution
                    if working_img.size != (new_width, new_height):
                        working_img = working_img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                    # Step 4: Apply High-Fidelity Filters
                    if selected_filter == "Black & White":
                        working_img = ImageOps.grayscale(working_img)
                    elif selected_filter == "Sepia Tone":
                        gray = ImageOps.grayscale(working_img)
                        working_img = ImageOps.colorize(gray, "#704214", "#C0B283")
                    elif selected_filter == "Gaussian Blur":
                        working_img = working_img.filter(ImageFilter.GaussianBlur(radius=5))
                    elif selected_filter == "Contour Sketch":
                        working_img = working_img.filter(ImageFilter.CONTOUR)
                    elif selected_filter == "Vibrant Saturation":
                        enhancer = ImageEnhance.Color(working_img)
                        working_img = enhancer.enhance(
