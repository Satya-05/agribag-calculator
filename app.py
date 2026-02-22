import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# Page configuration - looks good on phone and desktop
st.set_page_config(
    page_title="AgriBag Calculator",
    page_icon="🌾",
    layout="wide"
)

# Title and intro
st.title("🌾 AgriBag Calculator")
st.markdown("""
Upload a clear, straight-on photo of your notebook page  
(4 columns × 10 rows of handwritten bag weights like 72, 56.4, 56.9).  
The app will extract the numbers, sum each column, and give the grand total.
""")

# File uploader
uploaded_file = st.file_uploader(
    "Upload notebook page photo",
    type=["jpg", "jpeg", "png"],
    help="Best results: good lighting, page filling most of the frame, no shadows"
)

if uploaded_file is not None:
    try:
        # Read the uploaded file as bytes
        image_bytes = uploaded_file.read()
        
        # Open as PIL Image for display
        pil_image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to OpenCV format (BGR) for processing later
        img_cv = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        # Show the image
        st.subheader("Uploaded Notebook Page")
        st.image(pil_image, use_column_width=True, caption="Your uploaded photo")
        
        # Show basic image info (useful for debugging grid later)
        height, width, channels = img_cv.shape
        st.info(f"Image size: {width} × {height} pixels ({channels} channels)")
        
        # Placeholder for next steps (OCR, grid detection, etc.)
        st.success("Image loaded successfully! Ready for OCR extraction in the next update.")
        
        # Future: We'll add button here to "Process Weights"
        if st.button("Process Weights (Coming Soon)"):
            st.write("OCR processing will start here...")
            
    except Exception as e:
        st.error(f"Error reading image: {e}")
        st.info("Try uploading a different photo or check file format.")

else:
    st.info("Please upload a photo to begin.")