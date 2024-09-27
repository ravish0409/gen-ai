# Function to handle candidate login logic
import streamlit as st
from db_operations import *
from PIL import Image
import os
from docx import Document
from PyPDF2 import PdfReader
import base64
def handle_candidate_login(input_user, input_password):
    if input_user and input_password:
        data = fetch_candidate_data()
        user=data.loc[(data["username"] == input_user) & (data['password'] == input_password)]
        if user.size:
            st.session_state['candidate_login'] = True
            st.session_state['candidate_username'] = input_user
            st.session_state.candidate_id=int(user['id'].values[-1])
        else:
            st.error('Invalid username or password')
    else:
        st.error('Please fill in all fields')

# Function to handle candidate signup logic
def handle_candidate_signup(new_user, new_password):
    if new_user and new_password:
        if any(char in new_user for char in """ []'"!@#$%^&*()?|\/.,_+-={}:<>""") or new_user[0].isdigit():
            st.error("Username should not contain any special characters and should not start with a number")

        else:
            data = fetch_candidate_data()
            if data.loc[data['username'] == new_user].size:
                st.error('Username already exists. Please choose another.')
            else:
                values = (new_user, new_password)
                add_candidate(values)
                st.session_state['candidate_login'] = True
                st.session_state['candidate_username'] = new_user
                if len(data)>0:
                    st.session_state.candidate_id=int(data['id'].values[-1])+1
                else:
                    st.session_state.candidate_id=1
    else:
        st.error('Please fill in all fields')

# Candidate login form
def candidate_login_form():

    input_user = st.text_input('Enter username:', placeholder='Username', key='candidate_login_user')

    input_password = st.text_input('Password:', type='password', placeholder='Password', key='candidate_login_password')
    st.button('Login', on_click=handle_candidate_login, args=(input_user, input_password))

# Candidate signup form
def candidate_signup_form():
    new_user = st.text_input('Choose a username:', placeholder='Username', key='candidate_signup_user')
    new_password = st.text_input('Choose a password:', type='password', placeholder='Password', key='candidate_signup_password')
    st.button('Sign Up', on_click=handle_candidate_signup, args=(new_user, new_password))


def save_details(name,email,phone,picture,resume):
    if name and email and phone and picture and resume:
        st.session_state.resume=f'uploads/{resume.name}'
        image = Image.open(picture)
        image_path = os.path.join('images', f'{name}-{phone[:4]}.png')
        image.save(image_path)
        st.session_state.picture = image_path
        columns=('name','email','phone_number','picture','resume_path','all_fields_fill')
        values=(name,email,phone,st.session_state.picture,st.session_state.resume,1)
        update_candidate(columns,values,st.session_state.candidate_username)
        if 'page' not in st.session_state:
            st.session_state.page = 1
    else:
        st.error('Please fill in all fields')

def display_docx(file_path):
    doc = Document(file_path)
    for para in doc.paragraphs:
        st.write(para.text)

def display_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="670" height="900" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def show_job_posting(file_path,job):
    if file_path:
        if os.path.exists(file_path):
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.docx':
                with st.expander(f"job description", expanded=True):
                    display_docx(file_path)
            elif file_extension == '.pdf':
                with st.expander(f"Job description", expanded=True):
                    display_pdf(file_path)
            else:
                st.error("Unsupported file format. Please provide a path to a DOCX or PDF file.")
        else:
            st.error("File not found. Please check the file path and try again.")
    # def next_page():
#     if st.session_state.page==1:
#         if resume and text:
            
#             try:
#                 data=fetch_applied_candidate_data(text)
#                 st.session_state.token=text
#                 _,st.session_state.recruiter,st.session_state.id=st.session_state.token.split('1729')
#                 recruiter_data=fetch_job_data(st.session_state.recruiter)
#                 st.session_state.job_posting=recruiter_data.loc[recruiter_data['id']==int(st.session_state.id),'description'].values[0]
#                 st.session_state.resume=f'uploads/{resume.name}'
#                 st.session_state.page = 2
#                 st.session_state.role_list = ["Candidate"]
#             except:
#                 st.error("Invalid token")
#         else:
#             st.error("provide all info before proceeding.")
            
#     elif st.session_state.page==2:
#             if name and email and phone and picture:
#                 st.session_state.name = name
#                 st.session_state.email = email
#                 st.session_state.phone = phone
#                 image = Image.open(picture)
#                 image_path = os.path.join('images', f'{name}-{phone[:4]}.png')
#                 image.save(image_path)
#                 st.session_state.picture = image_path
#                 st.session_state.page = 3

#             else:
#                 st.error("Please fill in all fields and upload a picture.")
