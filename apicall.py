
import os
from openai import OpenAI
from dotenv import load_dotenv
import PyPDF2
from docx import Document
import json


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_text_from_pdf(pdf_file_path):
    text = ""
    try:
        with open(pdf_file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
    except Exception as e:
        print(f"Error reading PDF file: {e}")
    return text

def extract_text_from_docx(docx_file_path):
    text = ""
    try:
        doc = Document(docx_file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX file: {e}")
    return text



def extract_text_from_file(file_path):
    p,n=file_path.split('.')
    if n=='pdf':
        text = extract_text_from_pdf(file_path)
    else: 
        text = extract_text_from_docx(file_path)

    return text


def get_questions(job, resume):
    job_description = extract_text_from_file(job)
    candidate_details = extract_text_from_file(resume)
    
    prompt = f'''
    You are an AI assistant tasked with generating customized interview questions based on a candidate’s details and a job description.

    Context:

    Candidate Details: {candidate_details}
    Job Description: {job_description}
    Task: Create a list of up to 8 interview questions. The list should include the following predefined questions, tailored to the candidate’s details and job description, as well as any additional questions you deem relevant:

    1. What is your expected salary range?
    2. Can you share your date of birth?
    3. Do you have experience with [relevant skill from job posting]?
    4. What are your preferred work hours?
    5. Can you tell us about a challenging project you've worked on?

    Please ensure each question is customized based on the specific candidate and job requirements. Provide the final output as a numbered list of interview questions and only list the questions as output, nothing else.
    '''
    
    # API call to OpenAI
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        top_p=0.5
    )
    
    # Get the response and clean up the formatting
    raw_output = response.choices[0].message.content
    
    # Split into lines and clean up extra whitespace
    questions = [q.strip() for q in raw_output.split('\n') if q.strip() and q[0].isdigit()]

    return questions





def  get_score(job_file,convo):
    job=extract_text_from_file(job_file)
    prompt = f'''
    You are an expert interviewer and evaluator, tasked with assessing a candidate's performance based on their answers to the first round of interview questions, in alignment with the job description provided.

    Context:
    - Job Description: {job}
    - Candidate's Responses: {convo}


    Final Output:
    Provide only a final score out of 100, nothing else. eg: 85

    '''
    response = client.chat.completions.create(
    model="gpt-4",  # or "gpt-3.5-turbo" depending on your access
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0.3,  # Lower temperature for more accurate and consistent scoring
    top_p=1,          # Use all possible outputs
    )
    
    # Get the AI response and return it
    evaluation_output = response.choices[0].message.content
    return evaluation_output





