import sqlite3
import pandas as pd

# Initialize connection to the SQLite database



def get_db_connection():
    conn = sqlite3.connect('my_database.db')
    return conn
def create_database():
    conn = get_db_connection()  # This creates the database file
    cursor = conn.cursor()

    # Create a table called "users"
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT ,
        email TEXT ,
        phone_number TEXT,
        picture TEXT,
        conversation TEXT,
        resume_path TEXT,
        score INTEGER 
    )
    ''')
    
    conn.commit()
    conn.close()
# Fetch data from the database
def fetch_data():
    conn = get_db_connection()
    query = "SELECT id, name, email, phone_number, picture, conversation, resume_path, score FROM users order by score DESC"

    df = pd.read_sql(query, conn)
    conn.close()
    return df
def add_data( columns, values):
    """
    Insert data into specified columns of a table.
    
    Parameters:
    - table (str): The name of the table to insert data into.
    - columns (list): A list of column names where data will be inserted.
    - values (tuple): A tuple of values corresponding to the columns.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Dynamically build the column and value placeholders for the SQL query
    columns_str = ', '.join(columns)  # e.g., "name, email, phone_number"
    placeholders = ', '.join(['?' for _ in values])  # e.g., "?, ?, ?"
    
    # SQL query for inserting data
    query = f"INSERT INTO users ({columns_str}) VALUES ({placeholders})"
    
    try:
        # Execute the query with the provided values
        cursor.execute(query, values)
        conn.commit()
        print(f"Data inserted into users successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()
# Update the score for a specific user in the database
def update_score(user_id, new_score):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET score = ? WHERE id = ?", (new_score, user_id))
    conn.commit()
    conn.close()
