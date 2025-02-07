import pypdf
from streamlit_extras.stylable_container import stylable_container
import io
import streamlit as st

def edit_metadata():
    st.markdown(
        """
        <h1 style="text-align: center; color: #FFFFFF;">
            Welcome to Our <span style="color: red;">MetaData Garage</span>
        </h1>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
            """
            <p style="text-align: center; color: #555; font-size: 16px;">
                "Let's Dive into PDF Metadata"
            </p>
            """,
            unsafe_allow_html=True
        )
    st.markdown("""
    ##### 📝 Suggestion:  
    - **Edit with Caution:** Only edit metadata if necessary, and ensure it's accurate before saving.

    ---
    """)

    try:        
        uploaded_file = st.file_uploader("Upload File Here:", type=".pdf")
        
        if uploaded_file:
            pdf_reader = pypdf.PdfReader(uploaded_file)
            pdf_writer = pypdf.PdfWriter()

            # Append existing pages to a new writer object
            pdf_writer.append_pages_from_reader(pdf_reader)
            
            # Collect metadata details from user input
            document_title = st.text_input("🧪Please enter the title for the document:").strip()
            author_name = st.text_input("Please enter the author name:", autocomplete="")
            document_subject = st.text_input("Please enter the subject for the document:", autocomplete="")
            keywords_input = st.text_input("Please enter keywords for the document (separated by commas):", autocomplete="")
            modification_year_input = st.date_input("Please enter the Modification year:", value=None)

            # Create a dictionary to hold metadata information
            if document_title:
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
                    start_button = st.button("⚙️Start Editing")

                if start_button:
                        with st.spinner("Editing MetaData"):
                            metadata_dict = {
                                "/Title": document_title,
                                "/Author": author_name,
                                "/Subject": document_subject,
                                "/Keywords": keywords_input,
                                "/Modification": modification_year_input,
                            }
                            
                            pdf_writer.metadata = metadata_dict
                            
                            pdf_buffer = io.BytesIO()
                            pdf_writer.write(pdf_buffer)
                            pdf_buffer.seek(0)
                                
                            st.success("Metadata successfully edited!")
                            st.download_button("Download PDF", data=pdf_buffer, file_name=uploaded_file.name,use_container_width=True)
                    
            else:
                st.info("Title of PDF must be fulfilled for download.")
        else:
            st.info("Please select a file!")

    except PermissionError:
        st.error("Error: Permission denied when trying to save the file. Check your permissions.")
    except Exception as error:
        st.error(f"Something went wrong while saving the file: {error}")
        
if __name__ == "__main__":
    edit_metadata()