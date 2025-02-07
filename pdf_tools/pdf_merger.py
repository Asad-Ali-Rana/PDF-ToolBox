import streamlit as st
import io
import pypdf
from streamlit_extras.stylable_container import stylable_container
    
def combine_pdfs():
    st.markdown(
        """
        <h1 style="text-align: center; color: #FFFFFF;">
            Welcome to <span style="color: red;">PDF Merger</span>
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="text-align: center; color: #555; font-size: 16px;">
            "Combine PDF's effortlessly"
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""
    ##### 🎯 Tip:
    - **Clear Old Files**: Reset old files before uploading new ones.  
    ---
    """)

    try:
        # File uploader to upload multiple PDF files
        uploaded_files = st.file_uploader(
            "Upload PDF Files Here:",
            type=".pdf",
            accept_multiple_files=True
        )

        if uploaded_files:
            if len(uploaded_files) >= 2:
                pass
            else:
                st.info("**Upload Atleast two files for merging**")
            # Initialize session state for the merging queue if it doesn't exist
            if "merging_queue" not in st.session_state:
                st.session_state.merging_queue = []

            # Create a list of files not yet in the merging queue
            available_files = []
            for file in uploaded_files:
                if file.name not in st.session_state.merging_queue:
                    available_files.append(file.name)

            # Only display the dropdown if there are files left to add
            if available_files:
                selected_file = st.selectbox(
                    label="Select a PDF File to Merge as first or next file to the Queue:",
                    options=["Select a file"] + available_files
                )

                # Add the selected file to the queue via button
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
                    add_queue = st.button("Add to Queue +")
                if add_queue:
                    if selected_file != "Select a file" and selected_file not in st.session_state.merging_queue:
                        st.session_state.merging_queue.append(selected_file)
                        st.rerun() # immediate rerun to refresh the dropdown
                    else:
                        st.warning("Please select a valid file or avoid duplicates!")

            # Display the files in the merging queue
            if st.session_state.merging_queue:
                st.markdown("### Files in the Merging Queue:")
                for index, file in enumerate(st.session_state.merging_queue, start=1):
                    st.write(f"{index}. {file}")

            # Merge the files if there are at least two in the queue
            if len(st.session_state.merging_queue) >= 2:
                if st.button("🚀 Merge Now!"):
                    with st.spinner("Merging..."):
                        try:
                            pdf_merger = pypdf.PdfWriter()

                            # Add pages from each selected file to the PdfWriter
                            for queue_file in st.session_state.merging_queue:
                                for uploaded_file in uploaded_files:
                                    if uploaded_file.name == queue_file:
                                        uploaded_file.seek(0) # Reset stream before each read
                                        pdf_reader = pypdf.PdfReader(uploaded_file)
                                        for page in pdf_reader.pages:
                                            pdf_merger.add_page(page)

                            # Save merged PDF to a BytesIO buffer
                            pdf_buffer = io.BytesIO()
                            pdf_merger.write(pdf_buffer)
                            pdf_buffer.seek(0)

                            st.success("PDF successfully merged!")
                            st.download_button(
                                label="Download Merged PDF",
                                data=pdf_buffer,
                                file_name="Merged.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )

                            # Clear the merging queue
                            st.session_state.merging_queue.clear()
                        except Exception as error:
                            st.error(f"An error occurred during merging: {error}")
                if len(st.session_state.merging_queue) > 0:
                    if st.button("❌ Clear Queue!"):
                        st.session_state.merging_queue.clear()
                        st.rerun()
                        st.success("Queue Successfully Cleared!")    
    except PermissionError:
        st.error("Error: Permission denied. You do not have access to this file.")
    except Exception as error:
        st.error(f"An unexpected error occurred: {error}")
    
if __name__ == "__main__":
    combine_pdfs()
