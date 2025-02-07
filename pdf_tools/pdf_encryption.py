import pypdf
import io
import random
import streamlit as st
from streamlit_extras.stylable_container import stylable_container

def generate_password():
    try:
        uppercase_letters = [chr(i) for i in range(65, 91)]  # A-Z
        digits = [str(i) for i in range(10)]                  # 0-9
        special_characters = ['@', '#', '$', '%', '^', '&', '*',
                              '(', ')', '_', '+', '[', ']', ':',
                              '?', '|', '~', '-', '']
        
        combined_character_set = uppercase_letters + digits + special_characters
        password_length = 10
        
        # Ensure the character set is long enough for the desired password length
        while len(combined_character_set) < password_length:
            combined_character_set += combined_character_set
        
        # Generate random password
        password = ''.join(random.sample(combined_character_set, password_length))
        
        col1, col2, col3 = st.columns(3)
        
        if "password1" not in st.session_state:
            st.session_state.password1 = password
            
        with col1:    
            if st.button("Regenerate Password"):
                new_password = password
                st.session_state.password1 = new_password
        
        with col2:
            show_password_checkbox = st.checkbox("Show Password", key="show_password")
        
        with col3:
            if show_password_checkbox:
                st.write(f"Password: {st.session_state.password1}")
            else:
                st.write(f"Password: {'*' * 8}")
                
    except Exception as error:
        st.error(f"Something went wrong during password generation. Error: {error}")

def encrypt_pdf():
    """
    Encrypts a PDF file with AES-256 encryption.

    This function allows users to upload a PDF file and encrypt it using a user-defined password.
    If the file is already encrypted, a warning is displayed.

    Raises:
        PermissionError: If there are permission issues accessing the file.
    """
    
    # Display welcome message
    st.markdown(
        """
        <h1 style="text-align: center; color: #FFFFFF;">
            Welcome to <span style="color: red;">PDF Encryptor</span>
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="text-align: center; color: #555; font-size: 16px;">
            "Lock Your Files, Stay Secure"
        </p>
        """,
        unsafe_allow_html=True
    )
    st.markdown("""
    ##### 🛡️ Recommendation:  
    - **Use Built-in Generator:** Generate a strong password using our built-in password generator for better security.

    ---
    """)
    
    try:
        uploaded_file = st.file_uploader("Upload File Here:", type=".pdf")
        
        if uploaded_file:
            st.divider()
            pdf_reader = pypdf.PdfReader(uploaded_file)
            pdf_writer = pypdf.PdfWriter(clone_from=pdf_reader)
            
            if not pdf_reader.is_encrypted:
                st.markdown("#### Password Generator 🔑")
                generate_password()
                st.markdown("---")
                
                password_for_encryption = st.text_input(
                    "Please Enter the password for encrypting the file 👇🏻:",
                    type="password",
                    placeholder="Enter Here:"
                )
                
                if password_for_encryption:
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
                        start_encryption_button = st.button("Lock PDF Now 🔒")
                    
                    if start_encryption_button:
                        with st.spinner("Encrypting..."):
                            pdf_writer.encrypt(user_password=password_for_encryption, algorithm="AES-256")
                            binary_conversion_stream = io.BytesIO()
                            pdf_writer.write(binary_conversion_stream)
                            binary_conversion_stream.seek(0)
                            
                            encrypted_file_name = "Encrypted-" + uploaded_file.name
                            
                            st.success("File Successfully Encrypted!")
                            st.download_button(
                                "Download Encrypted File",
                                data=binary_conversion_stream,
                                file_name=encrypted_file_name,
                                use_container_width=True
                            )
                else:
                    st.info("Please Enter Password For encryption!")
            else:
                st.warning("**The file is already encrypted!**")
    
    except PermissionError:
        st.error("Error: Permission denied. You do not have access to this file!")
    
    except Exception as error:
        st.error(f"Error while accessing or encrypting the PDF file: {error}")

if __name__ == "__main__":
    encrypt_pdf()
