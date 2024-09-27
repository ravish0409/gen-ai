import sqlite3
import pandas as pd
import streamlit as st
# Initialize connection to the SQLite database



def get_db_connection():
    conn = sqlite3.connect('database.db')
    return conn

def create_recruiter_database():
    conn = get_db_connection()  # This creates the database file
    cursor = conn.cursor()

    # Create a table called "recruiter"
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recruiter (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT ,
        password TEXT,
        company TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

def add_recruiter(values):
    """
    Insert data into table.
    
    Parameters:
    - values (tuple): A tuple of values corresponding to the columns.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    placeholders = ', '.join(['?' for _ in values])  # e.g., "?, ?, ?"
    
    # SQL query for inserting data
    query = f"INSERT INTO recruiter (username, password,company) VALUES ({placeholders})"
    
    try:
        # Execute the query with the provided values
        cursor.execute(query, values)
        conn.commit()
        print(f"Data inserted into recruiter successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def fetch_recruiter_data():
    conn = get_db_connection()
    query = f"SELECT * FROM recruiter"

    df = pd.read_sql(query, conn)
    conn.close()
    return df

def create_job_database(recruiter):
    conn = get_db_connection()  # This creates the database file
    cursor = conn.cursor()

    # Create a table called "{recruiter}"
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {recruiter} (
        id INTEGER PRIMARY KEY ,
        job TEXT ,
        description TEXT ,
        token TEXT 
    )
    ''')
    
    conn.commit()
    conn.close()

def add_job(recruiter,values):
    """
    Insert data into table.
    
    Parameters:
    - values (tuple): A tuple of values corresponding to the columns.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    placeholders = ', '.join(['?' for _ in values])  # e.g., "?, ?, ?"
    
    # SQL query for inserting data
    query = f"INSERT INTO {recruiter} (id, job, description, token) VALUES ({placeholders})"
    
    try:
        # Execute the query with the provided values
        cursor.execute(query, values)
        conn.commit()
        print(f"Data inserted into {recruiter} successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def fetch_job_data(recruiter):
    conn = get_db_connection()
    query = f"SELECT id, job, description, token FROM {recruiter}"

    df = pd.read_sql(query, conn)
    conn.close()
    return df


def  delete_job(recruiter, job_id):

    conn=  get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {recruiter} WHERE id = ?", (job_id,))
    conn.commit()
    conn.close()    




def create_apply_candidates_table(token):
    conn = get_db_connection()  # This creates the database file
    cursor = conn.cursor()

    # Create a table called "users"
    m=f'''
    CREATE TABLE IF NOT EXISTS {token} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT ,
        email TEXT ,
        phone_number TEXT,
        picture TEXT,
        conversation TEXT,
        resume_path TEXT,
        score INTEGER 
    )
    '''
    cursor.execute(m)
    
    conn.commit()
    conn.close()
# Fetch data from the database
def fetch_applied_candidate_data(token):
    conn = get_db_connection()
    query = f"SELECT id, name, email, phone_number, picture, conversation, resume_path, score FROM {token} order by score DESC"

    df = pd.read_sql(query, conn)
    conn.close()
    return df
def add_applied_candidate_data( token, columns, values):
    """
    Insert data into table.
    
    Parameters:
    - token  (str): table name
    - columns (list): A list of column names where data will be inserted.
    - values (tuple): A tuple of values corresponding to the columns.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Dynamically build the column and value placeholders for the SQL query
    columns_str = ', '.join(columns)  # e.g., "name, email, phone_number"
    placeholders = ', '.join(['?' for _ in values])  # e.g., "?, ?, ?"
    
    # SQL query for inserting data
    query = f"INSERT INTO {token} ({columns_str}) VALUES ({placeholders})"
    
    try:
        # Execute the query with the provided values
        cursor.execute(query, values)
        conn.commit()
        print(f"Data inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def delete_jobs_apply_database(token):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = f"DROP TABLE {token}"
    cursor.execute(query)
    conn.commit()
    conn.close



#---------------------------------------------------#
# Create candidate table
def create_candidate_database():
    conn = get_db_connection()  # This creates the database file
    cursor = conn.cursor()

    # Create a table called "candidate"
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS candidate (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        name TEXT,
        email TEXT,
        phone_number TEXT,
        picture TEXT,
        resume_path TEXT,
        all_fields_fill INTEGER DEFAULT 0

    )
    ''')

    conn.commit()
    conn.close()

# Add candidate to database
def add_candidate(values):
    conn = get_db_connection()
    cursor = conn.cursor()

    placeholders = ', '.join(['?' for _ in values])  # e.g., "?, ?, ?"

    # SQL query for inserting data
    query = f"INSERT INTO candidate (username, password) VALUES ({placeholders})"

    try:
        # Execute the query with the provided values
        cursor.execute(query, values)
        conn.commit()
        print(f"Data inserted into candidate successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

# Update all fields for a candidate
def update_candidate(columns, values, username):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Ensure columns and values have the same length
    if len(columns) != len(values):
        raise ValueError("The number of columns must match the number of values.")
    
    # Prepare the base query
    query = "UPDATE candidate SET "
    
    # Dynamic column update logic
    set_clauses = [f"{column} = ?" for column in columns]
    
    # Join the set clauses to form the update part of the query
    query += ", ".join(set_clauses)
    
    # Add the WHERE clause to update the specific candidate
    query += " WHERE username = ?"

    try:
        # Execute the query with the provided parameters (values + username)
        cursor.execute(query, (*values, username))
        conn.commit()
        print(f"Data updated for candidate {username} successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

# Fetch candidate data from database
# @st.cache_data()
def fetch_candidate_data():
    conn = get_db_connection()
    query = f"SELECT * FROM candidate"

    df = pd.read_sql(query, conn)
    conn.close()
    return df

