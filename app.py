import streamlit as st
import time

# Function to handle page navigation
def next_page():
    if st.session_state.page==1:
        if job_posting and resume:
            st.session_state.page = 2
        else:
            st.error("Please upload both documents before proceeding.")
    elif st.session_state.page==2:
            if name and email and phone and picture:
                st.session_state.name = name
                st.session_state.email = email
                st.session_state.phone = phone
                st.session_state.picture = picture.read()
                st.session_state.page = 3
            else:
                st.error("Please fill in all fields and upload a picture.")

def save_uploaded_file(uploaded_file):
    
    with open(f"./uploads/{uploaded_file.name}", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File {uploaded_file.name} saved successfully!")

role = st.sidebar.selectbox("Select Role:", ["Candidate", "Admin"])

if role == "Candidate":
    
    
    if 'page' not in st.session_state:
        st.session_state.page = 1
    
    if st.session_state.page == 1:
        st.header("Upload Documents")
        job_posting = st.file_uploader("Upload Job Posting", type=['pdf', 'docx'])
        if job_posting: save_uploaded_file(job_posting) 
        resume = st.file_uploader("Upload Resume", type=['pdf', 'docx'])
        if resume: save_uploaded_file(resume)
        st.button("Next", on_click=next_page)
        
    elif st.session_state.page == 2:
        st.header("Candidate Information")
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        col1,col2=st.columns([1,1])
        # picture_upload = col1.file_uploader("Upload your picture", type=['jpg', 'png'])
        picture = col2.camera_input("Upload your picture")

        st.button("Start Interview", on_click=next_page)

    elif st.session_state.page == 3:
        st.header("page 3")

elif role == "Admin":
    st.title("Admin Portal")
