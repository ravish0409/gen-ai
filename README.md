

# Gen-AI Project: Automated Recruitment Portal

The Automated Recruitment Portal offers two main entry points, depending on the user's role: the **Recruiter Portal** and the **Candidate Portal**.

- Recruiters can log in, post job openings, generate unique tokens for candidates, and view detailed candidate data.
- Candidates can use these tokens to upload their resumes and provide personal information, which then leads them into an automated interview process.

## Table of Contents
- [System Flow](#system-flow)
  - [Recruiter Flow](#recruiter-flow)
  - [Candidate Flow](#candidate-flow)
  - [Interview Process](#interview-process)
- [Database and File Storage](#database-and-file-storage)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Usage](#usage)

## System Flow

![Online FlowChart   Diagrams Editor - Mermaid Live Editor_page-0001](https://github.com/user-attachments/assets/3abba203-4225-4b71-b08e-99d6e5ad9410) 

### Recruiter Flow

For recruiters, the process starts with logging into the system. If they're not logged in, the platform provides a login form. Upon successful login, recruiters are taken to the **Recruiter Dashboard**. From here, they can:

1. **Upload Job Postings**: Recruiters can post job openings that are stored in the system.
2. **Generate Tokens**: For each job posting, recruiters can generate a unique token for candidates.
3. **View Candidate Data**: Recruiters can view information submitted by candidates, such as resumes, personal details, and performance scores from the interview process.

All data from the system, including candidate information and job postings, is securely stored in a database for future access.

### Candidate Flow

Once a candidate receives a token from the recruiter, they can enter it into the **Candidate Portal** and upload their resume. The system ensures all input is valid before proceeding to the next steps.

- Candidates then enter their personal information and upload an image.
- Once all fields are filled in, the candidate moves to the **Interview Process**.

### Interview Process

During the **Interview Process**, the system retrieves a set of interview questions dynamically from an API, such as the **OpenAI API**.

- The questions are displayed to the candidate, who answers them in real-time.
- The system then evaluates the candidate's responses, calculates a score, and saves the results back to the database.
- All of this happens seamlessly, without any manual intervention required from the recruiter.

Once the interview is complete, the system ensures all candidate data, including their answers and scores, is stored securely in the database for recruiters to review.

## Database and File Storage

To handle data efficiently:

- Job postings, candidate information, and interview results are stored in a central **Database**.
- Resumes and images are stored in a **File Storage** system, ensuring easy access for recruiters when reviewing candidates.

## Prerequisites

Before you begin, ensure you have met the following requirements:
* You have a **Python 3.7+** environment
* You have a **GitHub** account
* You have an **OpenAI API** key

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
- Login using your recruiter credentials
- Upload job postings
- Generate tokens for candidates
- View and manage candidate data

### Candidate Interface
- Enter the provided token and upload your resume
- Fill in personal information and upload an image
- Complete the AI-generated interview process

