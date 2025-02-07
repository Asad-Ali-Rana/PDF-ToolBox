import pypdf
import streamlit as st
import io
from streamlit_extras.stylable_container import stylable_container

def remove_metadata():
    st.markdown(
        """
        <h1 style="text-align: center; color: #FFFFFF;">
            Welcome to the <span style="color: red;"> Metadata Eraser</span>
        </h1>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
            """
            <p style="text-align: center; color: #555; font-size: 16px;">
                "Wipe Out Unwanted File Details!"
            </p>
            """,
            unsafe_allow_html=True
        )
    st.markdown("""
    ##### 🧼 Tip:  
    - **Remove Sensitive Metadata:** Always remove sensitive metadata before sharing the PDF.

    ---
    """)

    try:
        uploaded_file = st.file_uploader("Upload Files Here:", type=".pdf")        
        if uploaded_file:
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
                    start_button = st.button("🗑️ Remove MetaData")
            if start_button:
                with st.spinner("Removing"):
                    pdf_reader = pypdf.PdfReader(uploaded_file)
                    pdf_writer = pypdf.PdfWriter()
                    
                    # Append pages from the original PDF to the writer
                    pdf_writer.append_pages_from_reader(pdf_reader)
                    
                    # Clear metadata from the PDF writer
                    pdf_writer.metadata = None
                    
                    binary_conversion = io.BytesIO()
                    pdf_writer.write(binary_conversion)
                    binary_conversion.seek(0)
                    
                    st.success("Metadata removed successfully!")
                    st.download_button("Download PDF Now", data=binary_conversion, file_name=uploaded_file.name,use_container_width=True)

    except PermissionError:
        st.error("Error: Permission denied. You do not have access to this file.")
    except Exception as error:
        st.error(f"An unexpected error occurred while removing metadata: {error}")

if __name__ == "__main__":
    remove_metadata()