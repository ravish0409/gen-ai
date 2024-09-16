import streamlit as st
import time
from PIL import Image
import os
from db_operations import fetch_data, update_score, create_database, add_data 
from apicall import get_questions,get_score
import random
from dotenv import load_dotenv
import pyperclip


load_dotenv()
user=os.getenv("user")
password=os.getenv("password")

create_database()
if "role_list" not in  st.session_state:

    st.session_state.role_list = ["Recruiter","Candidate"]

def display_user_info(user, user_index):
    with st.expander(f"User: {user['name']}", expanded=True):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if user['picture'] and user['picture'] != 'None':
                try:
                    st.image(user['picture'], width=150)
                except:
                    st.image("https://via.placeholder.com/150", width=150, caption="No image available")
            else:
                st.image("https://via.placeholder.com/150", width=150, caption="No image available")
        
        with col2:
            st.markdown(f"**Email:** {user['email']}")
            st.markdown(f"**Phone:** {user['phone_number']}")
            st.markdown(f"**Score:** {user['score']}")
        
        st.markdown("### Conversation")
        st.text_area(
            label="User Conversation",
            value=user['conversation'],
            height=150,
            disabled=True,
            key=f"conversation_{user_index}",
            label_visibility="collapsed"
        )
        
        st.markdown("### Resume")
        if user['resume_path']:
            filepath=user['resume_path']
            folder,filename=filepath.split('/')
            try: 
                with open(filepath, 'rb') as f:
                    file_data = f.read()
                    
                st.download_button(
                    label=f"Download {filename}",
                    data=file_data,
                    file_name=filename,
                    mime='application/octet-stream',
                    key=f"download_button_{user_index}_{filename}"
                )
            except:
                st.write("No resume available")

        else:
            st.warning("No resume available")
def next_page():
    if st.session_state.page==1:
        if resume and text:
            if text==st.session_state.token:
                st.session_state.job_posting=st.session_state.token.split('-')[-1]
                st.session_state.resume=f'uploads/{resume.name}'
                st.session_state.page = 2
            else:
                st.error("Invalid token")
        else:
            st.error("provide all info before proceeding.")
            
    elif st.session_state.page==2:
            if name and email and phone and picture:
                st.session_state.name = name
                st.session_state.email = email
                st.session_state.phone = phone
                image = Image.open(picture)
                image_path = os.path.join('images', f'{name}-{phone[:4]}.png')
                image.save(image_path)
                st.session_state.picture = image_path
                st.session_state.page = 3

            else:
                st.error("Please fill in all fields and upload a picture.")

def save_uploaded_file(uploaded_file):
    with open(f"./uploads/{uploaded_file.name}", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File {uploaded_file.name} saved successfully!")
if "show_token" not in st.session_state:
    st.session_state.show_token = False
def clicked():
    if job_posting: 
        st.session_state.show_token=True
        # st.session_state.role_list=["Candidate","Recruiter"]
        # st.session_state.page=1
    else:
        st.error("Please upload a job posting before proceeding.")


role = st.sidebar.selectbox("Select Role:", st.session_state.role_list)



if role == "Recruiter" :
    # st.session_state.role_list = ["Recruiter","Candidate"]

    
    if 'login' not in  st.session_state:
        st.session_state.login = False
    
    if st.session_state.login:
        col1,col2=st.columns([5,1])
        with col1:
            st.title("Recruiter Portal")
            st.markdown("---")
        with col2:
            if st.button("Logout"):
                st.session_state.login = False

                st.session_state.show_token=False
                
        col1,col2=st.columns([3,2])
        with col1:
            job_posting = st.file_uploader("Upload Job Posting", type=['pdf', 'docx'])
            if job_posting: save_uploaded_file(job_posting)


            st.button('Generate Token 🎫',on_click=clicked)
        #progress bar
      


        if  job_posting and st.session_state.show_token:
            with  col2:
                job_posting_path=f'uploads/{job_posting.name}'
                st.session_state.token=f'%token%-{job_posting_path}'
                progress_bar = col2.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.01)  # Simulate some delay during token generation
                    progress_bar.progress(percent_complete + 1)
                with st.container(border=True):
                    with st.chat_message("🎫"):
                        st.markdown(st.session_state.token)
                _,colt=st.columns([1,2])
                with  colt:

                    if st.button('Copy to Clipboard'):
                        pyperclip.copy(st.session_state.token)
                        st.success("Text copied to clipboard!")


        st.markdown("---")
        data = fetch_data()
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.subheader("User Selection")
            names = ['All'] + [f'{i}. {v}' for i,v in zip(data['id'],data['name'])]
            selected_name = st.selectbox("Select a user:", names)
            st.markdown("### Quick Stats")
            st.metric("Total Users", len(data))
            st.metric("Max Score", data['score'].max())
        
        with col2:
            st.subheader("User Information and Scoring")
            if selected_name == 'All':
                st.info("Displaying information for all users")
                for index, user in data.iterrows():
                    display_user_info(user, index)
            else:
                id=int(selected_name.split('. ')[0])
                selected_user = data[data['id'] == id].iloc[0]
                display_user_info(selected_user, id)

    else:
        st.title("Recruiter Portal")
        st.markdown("---")
        st.title('Login')
        with st.form('login form'):
            input_user=st.text_input('Enter username :',placeholder='Username')
            input_password=st.text_input('Password :', type='password',placeholder='Password')
            submit_button=st.form_submit_button('Login')

        if submit_button:
            if input_user == user and input_password == password:
                st.session_state.login = True
            else:
                st.error('Invalid username or password')



elif role == "Candidate" :
    
    st.title('Candidate Portal')
    st.markdown('---')
    if 'token' not in st.session_state:
        st.session_state.token=os.getenv('token')    
    if 'page' not in st.session_state:
        st.session_state.page = 1
    
    if st.session_state.page == 1:
        col1,col2=st.columns([1,12])
        with col1:
            st.markdown("# 🎫")
        with col2:
            text=st.text_input('Enter:',placeholder="Enter Token")

        resume = st.file_uploader("Upload your Resume", type=['pdf', 'docx'])
        if resume: save_uploaded_file(resume)
        st.button("Next", on_click=next_page)
        
    elif st.session_state.page == 2:
        st.header("Candidate Information")
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        col1,col2=st.columns([1,1])
        # picture_upload = col1.file_uploader("Upload your picture", type=['jpg', 'png'])
        picture = col2.camera_input("your picture")

        st.button("Start Interview", on_click=next_page)

    elif st.session_state.page == 3:
        if "messages" not in st.session_state:
            st.session_state.messages = []
            st.session_state.stm=''

        if 'questions' not in st.session_state:
            print("one time")
            try:
                st.session_state.questions = get_questions(st.session_state.job_posting,st.session_state.resume)+['do you like to share something']
            except:
                st.session_state.questions =[ 
                    "What is your expected salary range?",
                    "Can you share your date of birth?",
                    "Do you have experience in [skill from job posting]?",
                    "What are your preferred work hours?",
                    "Can you tell us about a challenging project you've worked on?",
                    'do you like to share something', 
                    ]
        if "question_index" not in st.session_state:
            st.session_state.question_index = 0  # To keep track of the current question

        # List of questions to be asked
        question_list = st.session_state.questions
        # question_list=[ 
        #     "What is your expected salary range?",
        #     "Can you share your date of birth?",
        #     "Do you have experience in [skill from job posting]?",
        #     "What are your preferred work hours?",
        #     "Can you tell us about a challenging project you've worked on?",
        #     'do you like to share something', 
        # ]

        def get_q(index):
            for i in question_list[index].split():
                yield i+' '
                time.sleep(0.05)
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
                st.session_state.stm+='Q'+current_question+"\n"
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.session_state.stm+='Answer: '+prompt+'\n'
                
                # Move to the next question
                st.session_state.question_index += 1
                time.sleep(0.4)
                with st.chat_message("system"):
                    st.write(get_q(st.session_state.question_index))
        else:
            # print(st.session_state.stm)

            if "score" not in st.session_state:
                try:
                    st.session_state.score = get_score(st.session_state.resume, st.session_state.stm)
                except:
                    st.session_state.score = random.randint(15, 40)


            if 'saved' not in st.session_state and 'score' in st.session_state:
                column = ['name', 'email', 'phone_number', 'picture', 'conversation', 'resume_path', 'score']
                values = (st.session_state.name, st.session_state.email, st.session_state.phone, 
                        st.session_state.picture, st.session_state.stm, st.session_state.resume, 
                        st.session_state.score)
                add_data(column, values)
                st.session_state.saved = 1
                st.success("thank you for participating!")
else:
    st.warning("Please login first")
