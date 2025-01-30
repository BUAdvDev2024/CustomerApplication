import sqlite3
from contextlib import contextmanager
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv('ENCRYPTION_KEY')
cipher_suite = Fernet(key)

@contextmanager
def get_cursor():
    """
    Context manager for obtaining a database cursor.
    
    Yields:
        sqlite3.cursor: The cursor to the database
    
    Raises:
        sqlite3.Error: If there is an error with the database
    """
    con = sqlite3.connect('instance/records.db')
    try:
        cursor = con.cursor()
        yield cursor  # Yield the cursor to the caller
        con.commit()
    except sqlite3.Error as e:
        if con:
            con.rollback()
        raise e
    finally:
        cursor.close()
        con.close()

def insert_dummy_data(dummy_data_path):
    """
    Adds dummy data to the database for testing purposes
    
    Args:
        data (str): The path to the dummy data
    
    Raises:
        sqlite3.Error: If there is an error with the database
    """
    with get_cursor() as cursor:

        with open(dummy_data_path, "r") as file:
            insert_statements = file.read().split(";")

            for statement in insert_statements:
                cursor.execute(statement)

            return cursor.rowcount > 0


        
def encrypt_data(data):
    """
    Encrypts the given data using Fernet encryption.
    
    Args:
        data (str): The data to encrypt.
    
    Returns:
        str: The encrypted data.
    """
    return cipher_suite.encrypt(str(data).encode()).decode()

def decrypt_data(data):
    """
    Decrypts the given data using Fernet encryption.
    
    Args:
        data (str): The data to decrypt.
    
    Returns:
        str: The decrypted data, or the original data if it is not encrypted.
    """
    try:
        return cipher_suite.decrypt(str(data).encode()).decode()
    except Exception:
        return data