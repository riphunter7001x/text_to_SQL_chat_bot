import sqlite3
from typing import Optional
from langchain_community.utilities import SQLDatabase


def create_database_connection(db_path: str = 'bank_database.db') -> Optional[sqlite3.Connection]:
    """
    Create a connection to the SQLite database.
    
    Args:
        db_path (str): Path to the SQLite database file. Defaults to 'bank_database.db'
    
    Returns:
        sqlite3.Connection: Database connection object or None if connection fails
    """
    try:
        # Establish a connection to the database (creates it if it doesn't exist)
        connection = sqlite3.connect(db_path)
        return connection
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_tables(connection: sqlite3.Connection):
    """
    Create necessary tables in the database.
    
    Args:
        connection (sqlite3.Connection): Active database connection
    """
    try:
        cursor = connection.cursor()
        
        # Create customers table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            account_number TEXT UNIQUE NOT NULL,
            balance REAL NOT NULL
        )
        ''')
        
        # Create transactions table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            transaction_type TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        )
        ''')
        
        # Commit the changes
        connection.commit()
        print("Tables created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")
        connection.rollback()

def close_connection(connection: sqlite3.Connection):
    """
    Close the database connection.
    
    Args:
        connection (sqlite3.Connection): Active database connection
    """
    if connection:
        connection.close()
        print("Database connection closed.")

# Create a connection to the database
db = SQLDatabase.from_uri("sqlite:///bank_database.db")
