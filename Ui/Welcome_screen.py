import streamlit as st

def welcome():
    st.write(
        '<h1 style="color:white;">Welcome to <span style="color:red;">PDF</span> ToolBox</h1>',
        unsafe_allow_html=True
    )
    WELCOME_TEXT = """
    Your ultimate solution for all your PDF needs. Designed to be simple, powerful, and efficient, PDF Tool Box helps you manage your PDF files effortlessly.

    ---

    ### 🔧 **Key Features at Your Fingertips**  
    1. **📁 Merge PDFs**  
    - Combine multiple PDFs into a single document for seamless organization.  
    
    2. **✂️ Split PDFs**  
    - Extract specific pages or divide large PDFs into smaller files.  

    3. **👁️ View Metadata**  
    - **View Metadata:** Inspect file details such as author, title, and creation date.   

    4. **🔒 PDF Lock**  
    - Add strong password protection to secure your PDF files.  
    - Prevent unauthorized access and protect sensitive information.  

    5. **🧹 Remove Metadata**  
    - **Remove Metadata:** Delete sensitive metadata to protect your privacy.   

    6. **🔓 PDF Unlock**  
    - Effortlessly unlock password-protected PDFs by providing the correct password.  
    - Remove existing encryption for easier access.  

    7. **📄 Word to PDF**  
    - Turn your Word documents into secure PDFs with our trusted tool.  
    
    8. **📄 PDF to Word**  
    - Extract content from PDFs with ease and convert it back into Word files.  

    9. **💧 Stamp & Watermark**  
    - Add personalized text or image watermarks to your PDFs for branding or security.  
    
    10. **✏️ Edit Metadata**   
    - **Edit Metadata:** Update or correct metadata information for better organization.  

    11. **🖼️ Image to PDF**  
    - Transform image files into professional PDFs in seconds.  

    ---

    ### 🎯 **Why Choose PDF Tool Box?**  
    ✅ **Ease of Use**: Intuitive interface for everyone, from beginners to pros.  
    ✅ **Speed**: Get results quickly without compromising quality.  
    ✅ **Security**: Built-in encryption features to keep your data safe.  
    ✅ **Customizability**: Tailored options to meet all your PDF management needs.  

    ---

    ### 🚀 **Get Started Now!**  
    ➡️ Use the **sidebar** to select a feature.  
    ➡️ Follow the simple steps to process your PDF files.  
    ➡️ Save time and achieve more with PDF Tool Box!  

    💡 **Pro Tip**: Bookmark this tool as your go-to solution for all things PDF!  
    """
    st.markdown(WELCOME_TEXT)
if __name__ == "__main__":
    welcome()