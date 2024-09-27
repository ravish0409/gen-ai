import streamlit as st
import time
from db_operations import *
from apicall import get_questions,get_score
import random
from dotenv import load_dotenv
import pyperclip
from streamlit_option_menu import option_menu
from streamlit_modal import Modal
from candidate_help import *
from recruiter_help import *


load_dotenv()


create_recruiter_database()

if "role_list" not in  st.session_state:

    st.session_state.role_list = ["Recruiter","Candidate"]

def validate(what,input):
    if what == "email":
        if not "@" in input and "." in input:
            st.error('Enter a valid email')
    elif  what == "phone":
        if not input.isdigit():
            st.error('Enter a valid phone number')
    
    elif  what == "username":
        if any(char in input for char in " !@#$%^&*()_+-={}:<>"):
            st.error(" Username should not contain any special characters")

    elif what== "name":
        if any(char in input for char in "!@#$%^&*()_+-={}:<>"):
            st.error("Name should not contain any special characters")
    
    elif what== 'phone':
        if len(input) != 10 and not input.isdigit():
            st.error('Enter a valid phone number')




            


def save_uploaded_file(uploaded_file):
    with open(f"./uploads/{uploaded_file.name}", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File {uploaded_file.name} saved successfully!")
if "show_token" not in st.session_state:
    st.session_state.show_token = False
def clicked():
    if job_posting and job_title: 
        data=fetch_job_data(st.session_state.username)
        
        if data.loc[data['job']==job_title].size:
            modal = Modal(key="dublicate error", title="Error")
            with modal.container():
                st.error('job already exist')
        else:
            if len(data)>0:
                id=int(data['id'].values[-1])+1
            else:
                id=1
            job_posting_path=f'uploads/{job_posting.name}'
            st.session_state.token=f'token1729{st.session_state.username}1729{id}'
            values=(id,job_title,job_posting_path,st.session_state.token)
            add_job(st.session_state.username,values)
            st.session_state.show_token=True
            st.session_state.job_title=job_title
            create_apply_candidates_table(st.session_state.token)

        # st.session_state.role_list=["Candidate","Recruiter"]
        # st.session_state.page=1
    else:
        # st.dialog("Please upload a job posting before proceeding.",width='small')

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
        #logout button
        with col2:
            st.button("⏪ Logout", on_click=lambda: st.session_state.update(
                {"login": False,
                "show_token": False,
                "role_list": ["Recruiter", "Candidate"]}
            ))
                # st.session_state.login = False
                # st.session_state.show_token=False
                # st.session_state.role_list = ["Recruiter","Candidate"]

        # allow to choose 'Post a Job' 'Candidate Profiles' section
        selected=option_menu(
            menu_title=None,
            options=['Post a Job','Candidate Profiles'],
            icons=['journal-plus','bi-people-fill'],
            default_index=0,
            orientation='horizontal',
            key='options',
        )
        if selected=='Post a Job':     
            col1,col2=st.columns([3,2])
            with col1:
                job_title=st.text_input('Enter the Job Title :',placeholder='Title')
                if job_posting:=st.file_uploader("Upload Job Posting", type=['pdf', 'docx']): 
                    save_uploaded_file(job_posting)


                st.button('Post the Job',on_click=clicked)
        
            if  job_posting and st.session_state.show_token:
                with  col2:
                
                    progress_bar = col2.progress(0)
                    for percent_complete in range(100):
                        time.sleep(0.01)  # Simulate some delay during token generation
                        progress_bar.progress(percent_complete + 1)
            #         with st.container(border=True):
            #             with st.chat_message("🎫"):
            #                 st.markdown(st.session_state.token)
            #         _,colt=st.columns([1,2])
            #         with  colt:

            #             if st.button('Copy to Clipboard',on_click=lambda:pyperclip.copy(st.session_state.token)): 
            #                 st.success("Text copied to clipboard!")

            st.markdown('---')
            
 
            st.markdown("### Your :blue-background[Previous] Job postings")
            jobs=fetch_job_data(st.session_state.username)
            # st.dataframe(jobs[['job','token']],hide_index=True,use_container_width=True)
            event = st.dataframe(
                jobs[['job','token']],
                use_container_width=True,
                hide_index=True,
                on_select="rerun",
                selection_mode="multi-row",
            )

            people = event.selection.rows
            if people:
                ids=jobs.iloc[people]['id'].values
                st.subheader("Selected jobs")
                cold1,cold2=st.columns([2,3])
                with cold1:
                    st.dataframe(jobs.iloc[people]['job'],hide_index=True,width=300)
                with cold2:
                    if st.button('Delete'):
                        for id in ids:
                            delete_job(st.session_state.username,int(id))
                            delete_jobs_apply_database(jobs.loc[jobs['id']==id,'token'].values[0])
                            st.rerun()
            else:
                st.markdown('---')
                st.info('Select to delete job postings')
                    



            # st.header("Selected members")

            
            # st.write(people)
            # filtered_df = jobs.iloc[people]
            # st.dataframe(
            #     filtered_df,
            #     use_container_width=True,
            # )

        else :
            users_data=fetch_job_data(st.session_state.username)
            job_list=users_data['job'].tolist()
            with st.container():
                st.subheader('Select a job post')
                selected_job=st.selectbox(" ",job_list)
            try:
                token=users_data.loc[users_data['job']==selected_job,'token'].values[0]
            except:
                token=None
                st.info(' No job postings available')


            if token:
                data = fetch_applied_candidate_data(token)
                col1,col2=st.columns([3,2])
                st.markdown("## :blue[Applied Candidates]")
                event = st.dataframe(
                    data[['name','email','phone_number','score']],
                    use_container_width=True,
                    hide_index=True,
                    on_select="rerun",
                    selection_mode="multi-row",
                )

                people = event.selection.rows
                if people:
                    st.divider()
                    st.subheader("Selected candidate/s")
                    cold1,cold2=st.columns([5,3])
                    with cold1:
                        st.dataframe(data.iloc[people][['name','email','phone_number','score']],hide_index=True,use_container_width=True)
                    with cold2:
                        st.info('download the selected  candidate/s')
                    st.divider()
                else:
                    st.markdown('---')
                    st.info('Select candidates!!')
                    st.markdown('---')



                col1, col2 = st.columns([1, 3])
                
                with col1:
                    st.subheader("Candidate Selection")
                    names = ['All'] + [f'{i}. {v}' for i,v in zip(data['id'],data['name'])]
                    selected_name = st.selectbox("Select a Candidate:", names)
                    st.markdown("### Quick Stats")
                    st.metric("Total Candidates", len(data))
                    st.metric("Max Score", data['score'].max())
                
                with col2:
                    st.subheader("Candidate Information and Scoring")
                    if selected_name == 'All':
                        st.info("Displaying information for all Candidates")
                        for index, user in data.iterrows():
                            display_user_info(user, index)
                    else:
                        id=int(selected_name.split('. ')[0])
                        selected_user = data[data['id'] == id].iloc[0]
                        display_user_info(selected_user, id)

    else:
        st.title("Recruiter Portal")
        st.markdown("---")
        
        selected=option_menu(
            menu_title=None,
            options=['LogIn','Sign Up'],
            icons=['bi-box-arrow-in-right','bi-person-plus-fill'],
            default_index=0,
            orientation='horizontal',
            key='loginoptions',
        )
        if  selected=='LogIn':
            login_form()
        else:
            signup_form()




elif role == "Candidate" :
    create_candidate_database() 
    if 'candidate_login' not in  st.session_state:
        st.session_state.candidate_login = False

    if  st.session_state.candidate_login:
        st.session_state.role_list = ["Candidate"]
        data=fetch_candidate_data()
        candidate_record=data.loc[data['id']==st.session_state.candidate_id]
        if int(candidate_record['all_fields_fill'].values[-1]):
            st.session_state.resume=candidate_record['resume_path'].values[-1]
            if 'page' not in st.session_state:
                st.session_state.page = 1
            if st.session_state.page == 1:
                col1,col2=st.columns([5,1])
                with col1:
                    st.title("Candidate Portal")
                    st.markdown("---")
                #logout button
                with col2:
                    st.button("⏪ Logout", on_click=lambda: st.session_state.update(
                        {"candidate_login": False,
                        "role_list": ["Recruiter", "Candidate"]}
                    ))
                recuiters_data=fetch_recruiter_data()
                all_company=recuiters_data['company'].tolist()
                col1,col2=st.columns(2)
                with col1:
                    company=st.selectbox('choose company',all_company)
                if company:
                    try:
                        recuiters_data_username=recuiters_data.loc[recuiters_data['company']==company]['username'].values[-1]
                        company_job_data=fetch_job_data(recuiters_data_username)
                        job_list=company_job_data['job'].tolist()
                        job=col2.selectbox('select job',job_list)
                        st.session_state.token,st.session_state.job_posting=company_job_data.loc[company_job_data['job']==job][['token','description']].values[-1]
                        
                        see=fetch_applied_candidate_data(st.session_state.token)
                        candidate_data=fetch_candidate_data()
                        current_cabdidate_number=candidate_data.loc[candidate_data['id']==st.session_state.candidate_id]['phone_number'].values[-1]
                        exist=see.loc[see['phone_number']==current_cabdidate_number].size
                        if  exist:
                            st.info('you already applied')
                            button_enable=True
                        else:
                            button_enable=False
                        show_job_posting(st.session_state.job_posting,job)
                    except:
                        st.info('no job available for this company')
                        button_enable=True
                         
                else:
                    st.write(' ')
                    st.info('No companies yet')
                st.button("Start interview",on_click= lambda:st.session_state.update({'page':2,}),disabled=button_enable)
                    



            elif st.session_state.page == 2:
                if "messages" not in st.session_state:
                    st.session_state.messages = []
                    st.session_state.stm=''

                if 'questions' not in st.session_state:
                    print("one time")
                    try:
                        st.session_state.questions = get_questions(st.session_state.job_posting,st.session_state.resume)+['do you like to share something']
                    except:
                        st.session_state.questions =[ 
                            "1. What is your expected salary range?",
                            "2. Can you share your date of birth?",
                            "3. Do you have experience in [skill from job posting]?",
                            "4. What are your preferred work hours?",
                            "5. Can you tell us about a challenging project you've worked on?",
                            '6. do you like to share something', 
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

                
                    try:
                        st.session_state.score = get_score(st.session_state.resume, st.session_state.stm)
                    except:
                        st.session_state.score = random.randint(15, 40)

                    if st.session_state.score:
                        cand_data=fetch_candidate_data()
                        candidate_details=cand_data.loc[cand_data['username']==st.session_state.candidate_username]
                        _,_,_,st.session_state.name, st.session_state.email, st.session_state.phone, st.session_state.picture,st.session_state.resume,_=candidate_details.values[-1]
                        column = ['name', 'email', 'phone_number', 'picture', 'conversation', 'resume_path', 'score']
                        values = (st.session_state.name, st.session_state.email, st.session_state.phone, 
                                st.session_state.picture, st.session_state.stm, st.session_state.resume, 
                                st.session_state.score)
                        add_applied_candidate_data(st.session_state.token,column, values)
                        st.session_state.score=0
                        st.success("thank you for participating!")
                        progress_bar = st.progress(0)
                        for percent_complete in range(100):
                            time.sleep(0.02)  # Simulate some delay during token generation
                            progress_bar.progress(percent_complete + 1)
                        st.session_state.page=1
                        st.session_state.messages = []
                        st.session_state.stm=''
                        st.session_state.question_index = 0
                        st.rerun()

        else:
            col1,col2=st.columns([5,1])
            with col1:
                st.title("Candidate Portal")
                st.markdown("---")
            #logout button
            with col2:
                st.button("⏪ Logout", on_click=lambda: st.session_state.update(
                    {"candidate_login": False,
                    "role_list": ["Recruiter", "Candidate"]}
                ))
            st.header("Candidate Information")

            name = st.text_input("Name",placeholder='Enter your name' )

            email = st.text_input("Email",placeholder=' Enter your email')

            phone = st.text_input("Phone", placeholder='Enter your phone number')


            col1,col2=st.columns([1,1])
            with col1:
                resume = st.file_uploader("Upload your Resume", type=['pdf', 'docx'])
                if resume: save_uploaded_file(resume)
            # picture_upload = col1.file_uploader("Upload your picture", type=['jpg', 'png'])
            picture = col2.camera_input("your picture")

            st.button("Save", on_click=save_details,args=(name,email,phone,picture,resume,))
           

    else:
        st.title("Candidate Portal")
        st.markdown("---")
        selected=option_menu(
            menu_title=None,
            options=['LogIn','Sign Up'],
            icons=['bi-box-arrow-in-right','bi-person-plus-fill'],
            default_index=0,
            orientation='horizontal',
            key='loginoptionscandidate',
        )
        if  selected=='LogIn':
            candidate_login_form()
        else:
            candidate_signup_form()
else:
    st.warning("Please login first")
