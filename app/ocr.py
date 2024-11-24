import streamlit as st
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import os

# Ensure Tesseract OCR is installed and accessible
# Set pytesseract path if needed, e.g., pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def ocr_tab(languages="eng+rus"):
    st.title("File Upload and OCR Application")
    st.write("Upload an image or PDF file, and the app will extract text using OCR.")

    uploaded_file = st.file_uploader("Upload a file (image or PDF)", type=["png", "jpg", "jpeg", "pdf"])

    if st.button("Run OCR"):
        if uploaded_file:
            file_type = uploaded_file.type
            st.write(f"Uploaded file type: {file_type}")

            try:
                if file_type in ["image/png", "image/jpeg", "image/jpg"]:
                    image = Image.open(uploaded_file)
                    st.image(image, caption="Uploaded Image", use_container_width=True)
                    st.write("Performing OCR...")
                    text = pytesseract.image_to_string(image, lang=languages)
                    st.subheader("Extracted Text:")
                    st.text(text)

                elif file_type == "application/pdf":
                    with open("temp_uploaded_file.pdf", "wb") as temp_pdf:
                        temp_pdf.write(uploaded_file.read())
                    
                    st.write("Converting PDF to images for OCR...")
                    images = convert_from_path("temp_uploaded_file.pdf")

                    text = ""
                    for i, img in enumerate(images):
                        st.image(img, caption=f"Page {i + 1}", use_column_width=True)
                        st.write(f"Performing OCR on Page {i + 1}...")
                        text += pytesseract.image_to_string(img) + "\n\n"
                    
                    os.remove("temp_uploaded_file.pdf")
                    st.subheader("Extracted Text:")
                    st.text(text)

                else:
                    st.error("Unsupported file format. Please upload an image or PDF file.")
            
            except Exception as e:
                st.error(f"An error occurred while processing the file: {e}")

# File upload form
# uploaded_file = st.file_uploader("Upload a file (image or PDF)", type=["png", "jpg", "jpeg", "pdf"])

# if uploaded_file:
#     file_type = uploaded_file.type
#     st.write(f"Uploaded file type: {file_type}")

#     try:
#         if file_type in ["image/png", "image/jpeg", "image/jpg"]:
#             # Process image file
#             image = Image.open(uploaded_file)
#             st.image(image, caption="Uploaded Image", use_column_width=True)
#             st.write("Performing OCR...")
#             text = pytesseract.image_to_string(image)
#             st.subheader("Extracted Text:")
#             st.text(text)

#         elif file_type == "application/pdf":
#             # Process PDF file
#             with open("temp_uploaded_file.pdf", "wb") as temp_pdf:
#                 temp_pdf.write(uploaded_file.read())
            
#             st.write("Converting PDF to images for OCR...")
#             images = convert_from_path("temp_uploaded_file.pdf")

#             text = ""
#             for i, img in enumerate(images):
#                 st.image(img, caption=f"Page {i + 1}", use_column_width=True)
#                 st.write(f"Performing OCR on Page {i + 1}...")
#                 text += pytesseract.image_to_string(img) + "\n\n"
            
#             # Clean up temporary file
#             os.remove("temp_uploaded_file.pdf")
#             st.subheader("Extracted Text:")
#             st.text(text)

#         else:
#             st.error("Unsupported file format. Please upload an image or PDF file.")
    
#     except Exception as e:
#         st.error(f"An error occurred while processing the file: {e}")