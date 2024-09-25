import streamlit as st
from db_operations import *

def handle_login(input_user, input_password):
    if input_user and input_password:
        data=fetch_recruiter_data()
        if data.loc[(data["username"]== input_user) & (data['password']==input_password)].size:
            st.session_state['login'] = True
            st.session_state['username'] = input_user
            st.session_state.role_list=["Recruiter"]
        else:
            st.error('Invalid username or password')
    else:
        st.error('Please fill in all fields')

# Function to handle signup logic
def handle_signup(new_user, new_password):
    
    if  new_user and new_password:
        if any(char in new_user for char in """ []'"!@#$%^&*()?|\/.,_+-={}:<>""") or new_user[0].isdigit():
            st.error(" Username should not contain any special characters and should not start with a number")

        else:
            data=fetch_recruiter_data()
            if  data.loc[data['username']==new_user].size:
                st.error('Username already exists. Please choose another.')
            else:
                values=(new_user, new_password)
                add_recruiter(values)
                st.session_state['login'] = True
                st.session_state['username'] = new_user
                st.session_state.role_list=["Recruiter"]
                create_job_database(new_user)
    else:
        st.error('Please fill in all fields')
        

# Login form
def login_form():
    st.title('Login')
    input_user = st.text_input('👤 Enter username:', placeholder='Username', key='login_user')

    input_password = st.text_input('🔒 Password:', type='password', placeholder='Password', key='login_password')
    st.button('Login', on_click=handle_login, args=(input_user, input_password))

# Signup form
def signup_form():
    st.title('Sign Up')
    new_user = st.text_input('👤 Choose a username:', placeholder='Username', key='signup_user')
    new_password = st.text_input('🔒 Choose a password:', type='password', placeholder='Password', key='signup_password')
    company=st.text_input("🏬 Company:",placeholder='Company')
    st.button('Sign Up', on_click=handle_signup, args=(new_user, new_password))
    

def display_user_info(user, user_index):
    with st.expander(f"Candidate: {user['name']}", expanded=True):
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
