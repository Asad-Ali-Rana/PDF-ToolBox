import io
import pypdf
import streamlit as st
from streamlit_extras.stylable_container import stylable_container

def decrypt_pdf():
    st.markdown(
        """
        <h1 style="text-align: center; color: #FFFFFF;">
            Welcome to <span style="color: red;">PDF Decryptor</span>
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="text-align: center; color: #555; font-size: 16px;">
            "Unlock Your PDF Instantly!"
        </p>
        """,
        unsafe_allow_html=True
    )
    st.markdown("""
    ##### 🔓 Advice:  
    - **Authorized Access Only:** Ensure you have permission before decrypting any PDF.

    ---
    """)

    try:
        uploaded_file = st.file_uploader("Upload File Here!", type=".pdf")
        
        if uploaded_file:
            st.divider()
            pdf_reader = pypdf.PdfReader(uploaded_file)
            
            if pdf_reader.is_encrypted:
                st.markdown("#### Enter Password:")
                password_guide = "Provide the password used when encrypting or locking the file."
                user_password = st.text_input("", help=password_guide, type="password", placeholder="Enter Here:")
                

                if user_password:
                    with stylable_container(
                        key="encrypt_pdf",
                        css_styles="""
                        button {
                            background-color: red;
                            color: white;
                            border-radius: 25px;
                        }
                        """,
                    ):
                        start_decryption_button = st.button("Unlock PDF Now 🔑")
                
                    # Attempt to decrypt the PDF with the provided password
                    if start_decryption_button:
                        with st.spinner("Decrypting"):
                            if pdf_reader.decrypt(user_password):
                                pdf_writer = pypdf.PdfWriter()
                                
                                # Add all pages from the decrypted reader to the writer
                                for page in pdf_reader.pages:
                                    pdf_writer.add_page(page)

                                binary_conversion_stream = io.BytesIO()
                                pdf_writer.write(binary_conversion_stream)
                                binary_conversion_stream.seek(0)

                                decrypted_file_name = "Decrypted-" + uploaded_file.name
                                st.success("File successfully unlocked!")
                                
                                # Provide a download button for the decrypted file
                                st.download_button("Download Unlocked File", data=binary_conversion_stream, file_name=decrypted_file_name,use_container_width=True)
                            else:
                                st.warning("**Incorrect password. Please try again!**")
            else:
                st.warning("**File Already Unlocked or Encrypted!**")
    
    except PermissionError:
        st.error("Error: Permission denied. You do not have access to this file.")
    
    except Exception as error:
        st.error(f"Error while accessing or decrypting the PDF file: {error}")

if __name__=="__main__":
    decrypt_pdf()
