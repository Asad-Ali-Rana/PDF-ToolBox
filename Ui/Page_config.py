import streamlit as st

def config():
    st.set_page_config(
    page_title="PDF ToolBox",
    page_icon="assets/favicon.png",
    initial_sidebar_state="auto",
    menu_items = None
    )
    hide_st_style = """
                <style>
                MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    
if __name__ == "__main__":
    config()