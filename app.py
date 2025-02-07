import streamlit as st
import streamlit_option_menu as menu
from Ui import welcome, config
from pdf_tools import combine_pdfs
from pdf_tools import extract_metadata
from pdf_tools import crop_pdf
from pdf_tools import encrypt_pdf
from pdf_tools import decrypt_pdf
from pdf_tools import remove_metadata
from pdf_tools import apply_watermark_or_stamp
from pdf_tools import edit_metadata
from pdf_tools import convert_multiple_images_to_pdf

def main():
    
    # Configure the application settings
    config()
    
    with st.sidebar:
        selected_option = menu.option_menu(
            menu_title="PDF ToolBox",
            options=[
                "Home",
                "PDF Merger",
                "View MetaData",
                "PDF Splitter",
                "Protect PDF",
                "Unlock Locked PDF",
                "Remove Metadata",
                "Stamp & Watermark",
                "Edit MetaData",
                "Image to PDF",
            ],
            default_index=0,
            menu_icon="tools",
            icons=[
                "house",
                "intersect",
                "braces",
                "crop", 
                "shield-lock",
                "unlock-fill", 
                "eraser", 
                "droplet",
                "code",
                "card-image",
            ]
        )
        st.write("---")
        st.write("Developed by Muhammad Asad ❤️")
    
    # Handle user selection from the sidebar menu
    if selected_option == "Home":
        welcome()
    elif selected_option == "PDF Merger":
        combine_pdfs()
    elif selected_option == "View MetaData":
        extract_metadata()
    elif selected_option == "PDF Splitter":
        crop_pdf()
    elif selected_option == "Protect PDF":
        encrypt_pdf()
    elif selected_option == "Unlock Locked PDF":
        decrypt_pdf()
    elif selected_option == "Remove Metadata":
        remove_metadata()
    elif selected_option == "Stamp & Watermark":
        apply_watermark_or_stamp()
    elif selected_option == "Edit MetaData":
        edit_metadata()
    else:
        convert_multiple_images_to_pdf()  
main()
