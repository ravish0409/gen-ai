

# Gen-AI Project: Automated Recruitment Portal

The Automated Recruitment Portal offers two main entry points, depending on the user's role: the **Recruiter Portal** and the **Candidate Portal**.

- Recruiters can create accounts, post job openings, manage candidates for specific roles, and use auto-generated scores by LLM to evaluate applicants.
- Candidates can sign up, log in, complete their profile, and participate in an automated interview process for available job postings.

## Table of Contents
- [System Flow](#system-flow)
  - [Recruiter Flow](#recruiter-flow)
  - [Candidate Flow](#candidate-flow)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Usage](#usage)

## System Flow

![flowchart_page-0001](https://github.com/user-attachments/assets/e68424d8-0e03-4aad-a3a0-eb886d306488)


### Recruiter Flow

1. **Sign Up/Login**: Recruiters can create an account or log in to an existing one.
2. **Post a Job**: 
   - Enter job title
   - Upload job posting document (PDF or DOCX)
   - System generates a unique token for the job
3. **View Previous Job Postings**: 
   - See a list of all posted jobs
   - Option to delete job postings
4. **View Candidate Profiles**:
   - Select a specific job posting
   - View list of applied candidates with their scores
   - Access detailed information for each candidate

### Candidate Flow

1. **Sign Up/Login**: Candidates can create an account or log in to an existing one.
2. **Complete Profile**:
   - Enter personal information (name, email, phone)
   - Upload resume (PDF or DOCX)
   - Take or upload a picture
3. **Apply for Jobs**:
   - Select a company and available job posting
   - Participate in an automated interview process
4. **Interview Process**:
   - Answer a series of questions generated based on the job posting and resume
   - System calculates a score based on the answers

## Features

- User authentication for both recruiters and candidates
- Job posting management for recruiters
- Automated interview process for candidates
- Integration with OpenAI API for generating interview questions and scoring responses
- File upload functionality for resumes and profile pictures
- Database storage for user information, job postings, and application data

## Installation

To install Gen-AI, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/ravish0409/gen-ai.git
   cd gen-ai
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the root directory of the project.

2. Add your OpenAI API key to the `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Running the Application

To run Gen-AI, follow these steps:

1. Ensure you're in the project directory and your virtual environment is activated (if you're using one).

2. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

3. Open your web browser and navigate to the URL displayed in the terminal (usually `http://localhost:8501`).

## Usage

The application has two main interfaces:

### Recruiter Interface
- Sign up or log in using your credentials
- Post new job openings by providing job titles and uploading job descriptions
- View and manage previous job postings
- Access candidate profiles and their interview results for each job posting

### Candidate Interface
- Sign up or log in using your credentials
- Complete your profile by providing personal information, uploading a resume, and adding a profile picture
- Browse available job postings from different companies
- Participate in automated interviews for selected job postings
- Receive immediate feedback and scoring after completing the interview process

