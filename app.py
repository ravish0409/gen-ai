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
        if "messages" not in st.session_state:
            st.session_state.messages = []

        if "question_index" not in st.session_state:
            st.session_state.question_index = 0  # To keep track of the current question

        # List of questions to be asked
        question_list = [ 
            "What is your expected salary range?",
            "Can you share your date of birth?",
            "Do you have experience in [skill from job posting]?",
            "What are your preferred work hours?",
            "Can you tell us about a challenging project you've worked on?",
            'Rate this project on a scale of 1-5.', 
        ]

        # Function to display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # If there are still questions left to ask
        if st.session_state.question_index < len(question_list)-1:
            current_question = question_list[st.session_state.question_index]
            
            # Show the current question in the chat
            with st.chat_message("system"):
                st.markdown(current_question)

            # Get user's response
            if prompt := st.chat_input("Enter your answer"):
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                # Add both question and user response to chat history
                st.session_state.messages.append({"role": "system", "content": current_question})
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                # Move to the next question
                st.session_state.question_index += 1
                with st.chat_message("system"):
                    st.markdown(question_list[st.session_state.question_index])
        else:
            # st.session_state.messages.append({"role": "system", "content": question_list[st.session_state.question_index]})
            # st.session_state.messages.append({"role": "user", "content": prompt})
            st.write("You have answered all the questions. Thank you!")
elif role == "Admin":
    st.title("Admin Portal")
    st.write(st.session_state.messages)