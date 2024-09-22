import sqlite3
import pandas as pd

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
        password TEXT 
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
    query = f"INSERT INTO recruiter (username, password) VALUES ({placeholders})"
    
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
    query = f"SELECT id, username, password FROM recruiter"

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

def update_job_description(recruiter, job_id, new_description):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE {recruiter} SET description = ? WHERE id = ?", (new_description, job_id))
    conn.commit()
    conn.close()


def create_database(token):
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
def fetch_data(token):
    conn = get_db_connection()
    query = f"SELECT id, name, email, phone_number, picture, conversation, resume_path, score FROM {token} order by score DESC"

    df = pd.read_sql(query, conn)
    conn.close()
    return df
def add_data( token, columns, values):
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
        print(f"Data inserted into {token} successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()
# Update the score for a specific user in the database
def update_score(token,user_id, new_score):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE {token} SET score = ? WHERE id = ?", (new_score, user_id))
    conn.commit()
    conn.close()
