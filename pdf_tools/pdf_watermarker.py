import pypdf
from PIL import Image
import img2pdf
import streamlit as st
import io
from streamlit_extras.stylable_container import stylable_container

def resize_image(image_file):
    """
    Resizes an uploaded image to fixed dimensions and converts it to PDF format.

    Parameters:
    image_file (file-like object): The uploaded image file.

    Returns:
    BytesIO: A BytesIO object containing the converted PDF data or None if an error occurs.
    """
    
    try:
        uploaded_image = Image.open(image_file)

        if uploaded_image.mode in ("RGBA", "LA"):
            uploaded_image = uploaded_image.convert("RGB")

        resized_image = uploaded_image.resize((200, 200))

        image_memory = io.BytesIO()
        resized_image.save(image_memory, format="png")

        pdf_memory = io.BytesIO()
        converted_pdf_data = img2pdf.convert(image_memory.getvalue())
        pdf_memory.write(converted_pdf_data)
        pdf_memory.seek(0)

        return pdf_memory

    except PermissionError:
        st.error("**Error: Permission denied while accessing or saving the image.**")
        return None
    except Exception as error:
        st.error(f"An error occurred while resizing the image: {error}")
        return None

def load_watermark_stamp(apply_as_stamp, pdf_stamp, pdf_file):
    """
    Applies a watermark or stamp to each page of a PDF using an image converted to a PDF.

    Parameters:
    apply_as_stamp (bool): If True, the image is added as a stamp (overlays content).
                           If False, the image is added as a watermark (underlays content).
    pdf_stamp (BytesIO): The PDF data containing the stamp or watermark.
    pdf_file (file-like object): The original PDF file to which the stamp or watermark will be applied.
    """
    try:
        stamp_reader_page = pypdf.PdfReader(pdf_stamp).pages[0]
        pdf_writer = pypdf.PdfWriter(clone_from=pdf_file)

        for page in pdf_writer.pages:
            page.merge_page(stamp_reader_page, over=apply_as_stamp)

        binary_output = io.BytesIO()
        pdf_writer.write(binary_output)
        binary_output.seek(0)

        output_file_name = pdf_file.name
        
        st.success("File created successfully! 👌")
        
        st.download_button(
            "🔧 Download File",
            data=binary_output,
            file_name=output_file_name,
            use_container_width=True
        )

    except PermissionError:
        st.error("Error: Permission denied while accessing or saving the PDF.")

    except Exception as error:
        st.error(f"An error occurred while applying watermark/stamp: {error}")


def apply_watermark_or_stamp():
    st.markdown(
    """
    <h1 style="text-align: center; color: #FFFFFF;">
    Welcome to <span style="color: red;">PDF Stamper & Watermarker</span>
    </h1>
    """,
    unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="text-align: center; color: #555; font-size: 18px;">
            "Make Your PDFs Truly Yours!"
        </p>
        """,
        unsafe_allow_html=True
    )
    st.markdown("""
    ##### 🌊 Suggestion:  
    - **Choose Clear Stamps/Watermarks:** Ensure that the stamp or watermark does not obstruct important content in the PDF.
    ---
    """)
    try:
        option_selection = st.selectbox("Select an Option: ", options=["Stamp on PDF", "Use Watermark"])
        image_upload = st.file_uploader("Upload Image for Stamp or Watermark: ", type=".png")       
        st.info("**Upload an image and a PDF to start customizing your document.**")
        if image_upload:
            pdf_data = resize_image(image_upload)
            st.divider()
            pdf_file_path = st.file_uploader("Upload PDF Here: ", type=".pdf")

            if pdf_file_path:
                st.divider()
                with stylable_container(
                    key="remove_metdata",
                    css_styles="""
                    button {
                        background-color: red;
                        color: white;
                        border-radius: 25px;
                    }
                    """,
                ):
                    start = st.button("Run 🚀")
                if start:
                    with st.spinner("Working"):
                        is_stamp = option_selection == "Stamp on PDF"
                        load_watermark_stamp(apply_as_stamp=is_stamp, pdf_stamp=pdf_data, pdf_file=pdf_file_path)

    except Exception as main_error:
        st.error(f"Something went wrong in apply_watermark_or_stamp: {main_error}")

if __name__ == "__main__":
    apply_watermark_or_stamp()
