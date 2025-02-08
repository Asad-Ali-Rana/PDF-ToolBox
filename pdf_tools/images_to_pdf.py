import img2pdf
from streamlit_extras.stylable_container import stylable_container
import streamlit as st

def convert_multiple_images_to_pdf():
        
    st.markdown(
            """
            <h1 style="text-align: center; color: #FFFFFF;">
                Welcome to Conversion of <span style="color: red;">Image 2 PDF</span>
            </h1>
            """,
            unsafe_allow_html=True
        )
    st.markdown(
            """
            <p style="text-align: center; color: #555; font-size: 16px;">
                "Convert Images to PDFs in a Snap!"
            </p>
            """,
            unsafe_allow_html=True
        )
    st.markdown("""
    #####   🔍 Reminder:  
    - **Verify Image Quality:** Double-check image resolution and format before converting to PDF to ensure the best results.

    ---
    """)
    supported_image_types = ["png", "jpg", "jpeg", "ico"]

    uploaded_files = st.file_uploader("Upload Image Files: ", type=supported_image_types, accept_multiple_files=True)

    if uploaded_files:
        image_file_paths = []
        for uploaded_file in uploaded_files:
            image_file_paths.append(uploaded_file.getvalue())
            
        with stylable_container(
                key="button_key",
                css_styles="""
                button {
                    background-color: red;
                    color: white;
                    border-radius: 25px;
                }
                """,
                ):
                    start_button = st.button("⚙️ Convert to PDF")

        if start_button:

            try:
                with st.spinner("Converting"):
                    converted_pdf_data = img2pdf.convert(image_file_paths,rotation=img2pdf.Rotation.ifvalid)
                    image_file_paths.clear()
                    st.success("PDF created successfully! 👏")
                    st.download_button("Download PDF 💾", data=converted_pdf_data,
                                        file_name=f"image.pdf",
                                        mime="application/pdf")
                if st.button("❌ Clear Queue!"):
                    image_file_paths.clear()
                    st.rerun()
                    st.success("Queue Successfully Cleared!")  
            except Exception as e:
                st.error(f"An error occurred during PDF conversion: {e}")

if __name__ == "__main__":
    convert_multiple_images_to_pdf()
