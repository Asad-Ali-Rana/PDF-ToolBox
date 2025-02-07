import pypdf
import streamlit as st
import io
from zipfile import ZipFile

def crop_pdf():
    # Header Section
    st.markdown(
        """
        <h1 style="text-align: center; color: #FFFFFF;">
            Welcome to Our <span style="color: red;">PDF Croper</span>
        </h1>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <p style="text-align: center; color: #555; font-size: 16px;">
            "Split, Download, Simplify!"
        </p>
        """,
        unsafe_allow_html=True
    )
    st.markdown("""
    ##### ✂️ Advice:  
    - **Keep Backup:** Always maintain a backup of the original PDF before cropping or splitting.

    ---
    """)

    try:
        # Get the PDF file path from the user
        uploaded_file = st.file_uploader("Upload File Here: ", type=".pdf")
        st.divider()
        
        if uploaded_file:
            pdf_reader = pypdf.PdfReader(uploaded_file)
            total_pages = len(pdf_reader.pages)

            if total_pages > 1:
                max_page_index = total_pages - 1
                column1, column2 = st.columns(2)
                
                # Get the start and end range for splitting
                with column1:
                    start_page_index = st.number_input('🌟 Start page number:', min_value=0, max_value=max_page_index, step=1)
                with column2:
                    end_page_index = st.number_input('✨ End page number:', min_value=start_page_index + 1, max_value=total_pages, step=1)
                
                split_option = st.radio(label="Select Option",
                                        options=("1. Split the PDF pages and store it into one PDF",
                                                 "2. Split Pages into Separate PDFs"))
                
                # Button to start splitting
                st.divider()
                if split_option == "1. Split the PDF pages and store it into one PDF":
                    if st.button("🚀 Start"):
                        split_into_single_pdf(pdf_reader, start_page_index, end_page_index)
                else:
                    if st.button("🚀 Start"):
                        split_into_multiple_pdfs(pdf_reader, start_page_index, end_page_index)

            else:
                st.warning("The PDF must be longer than 1 page to perform cropping!")
    
    except PermissionError as permission_error:
        st.error(f"Error: You do not have permissions to access or modify the PDF file. Error details: {permission_error}")
    except Exception as general_error:
        st.error(f"Something went wrong. Error: {general_error}")

def split_into_single_pdf(pdf_reader, start_page_index, end_page_index):
    """Handles splitting into a single PDF file."""
    pdf_writer = pypdf.PdfWriter()
    
    with st.spinner("Splitting..."):
        for page_index in range(start_page_index, end_page_index):
            page = pdf_reader.pages[page_index]
            pdf_writer.add_page(page)

        binary_output = io.BytesIO()
        pdf_writer.write(binary_output)
        binary_output.seek(0)
        
        st.download_button("Download File", data=binary_output, file_name="split_pdf.pdf",use_container_width=True)
        st.success("PDF pages split successfully into a single file!")

def split_into_multiple_pdfs(pdf_reader, start_page_index, end_page_index):
    """Handles splitting into multiple separate PDF files."""
    zip_output = io.BytesIO()
    
    with ZipFile(zip_output, "w") as zip_file:
        for page_index in range(start_page_index, end_page_index):
            page_nums = page_index
            pdf_writer = pypdf.PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[page_index])
            
            with io.BytesIO() as page_buffer:
                pdf_writer.write(page_buffer)
                page_buffer.seek(0)
                page_nums+=1
                zip_file.writestr(f"page_{page_nums}.pdf", page_buffer.read())
    zip_output.seek(0)  # Critical for valid ZIP
    st.download_button("Download", data=zip_output, file_name="split_pages.zip",use_container_width=True)

if __name__ == "__main__":
    crop_pdf()
