import pypdf
import streamlit as st

def extract_metadata():
    st.markdown(
            """
            <h1 style="text-align: center; color: #FFFFFF;">
                Welcome to Your <span style="color: red;">MetaData Viewer</span>
            </h1>
            """,
            unsafe_allow_html=True
        )
    st.markdown(
            """
            <p style="text-align: center; color: #555; font-size: 16px;">
                "Reveal File Metadata Fast!"
            </p>
            """,
            unsafe_allow_html=True
    )
    st.markdown("""
    ##### 📋 Best Practice:  
    - **Verify Metadata Details**: Double-check metadata for accuracy before sharing the document.  

    ---
    """)


        
    try:
        uploaded_file = st.file_uploader("Upload File Here:", type=".pdf",key="file_upload")
        if uploaded_file:
            metadata_choice = st.radio(label="Select Format", options=["1. User-friendly format", "2. Developer-friendly format"])
            st.divider()
            st.markdown("### ***Metadata***:")
            with st.spinner("Extracting"):
                pdf_reader = pypdf.PdfReader(uploaded_file)
                if metadata_choice == "1. User-friendly format":
                    metadata = pdf_reader.metadata
                    
                    # Display key-value pairs of metadata or indicate absence of data
                    if metadata:
                        for key, value in metadata.items():
                            value_display = value if value else "Not Available!"
                            
                        # Display the key with styled markdown
                            st.markdown(
                                f"- <span style='color:red; font-weight:bold;'>{key}</span>: <span style='color:white; font-weight:bold;'>{value_display}</span>",
                                unsafe_allow_html=True
                                )
                        st.divider()
                    else:
                        st.info("No metadata found!")
                else:
                    # Print raw metadata for developers
                    st.write(pdf_reader.metadata)

    except PermissionError:
        st.error("Error: Permission denied when trying to access the file. Check your permissions.")
    except Exception as error:
        st.error(f"Something went wrong while extracting metadata. Error: {error}")
        
if __name__ == "__main__":
    extract_metadata()