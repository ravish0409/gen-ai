import streamlit as st
import time


def next_page():

    if job_posting and resume:
        st.session_state.page+=1
    else:
        st.error("Please upload both documents before proceeding.")
    
def save_uploaded_file(uploaded_file):
    if uploaded_file is not None:
       
        with open(f"./uploads/{uploaded_file.name}", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"File {uploaded_file.name} saved successfully!")



role = st.sidebar.selectbox("Select Role:", ["Candidate", "Admin"])

if role == "Candidate":
    st.title("Candidate Portal")
    
    if 'page' not in st.session_state:
        st.session_state.page = 1
    
    if st.session_state.page == 1:
        st.header("Upload Documents")
        job_posting = st.file_uploader("Upload Job Posting (PDF/DOCX)", type=['pdf', 'docx'])
        resume = st.file_uploader("Upload Candidate Resume (PDF/DOCX)", type=['pdf', 'docx'])
        if job_posting and resume:
            time.sleep(.5)
            save_uploaded_file(job_posting)
            save_uploaded_file(resume)
        m=st.button("Next", on_click=next_page)
    
    elif st.session_state.page == 2:
        st.markdown("# page 2")

elif role == "Admin":
    st.title("Admin Portal")
