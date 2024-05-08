import sqlite3
import os

DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def generate_test_data(num_contacts):
    """Generate test data for the contacts table."""
    db = connect_db()

    # Add "favorite class" column to table if it doesn't already exist
    db.execute('''ALTER TABLE contacts ADD COLUMN favorite TEXT''')
    db.commit()

    # Add "favorite moment" column to table if it doesn't already exist
    db.execute('''ALTER TABLE contacts ADD COLUMN moment TEXT''')
    db.commit()
    
    for i in range(num_contacts):
        name = f'Test Name {i}'
        phone = f'123-456-789{i}'
        favorite = f'My favorite class was CIT225{i}' # Add favorite class
        moment = f"My favorite moment was graduating{i}' # Add favorite moment
        db.execute('INSERT INTO contacts (name, phone, favorite, moment) VALUES (?, ?, ?, ?)', (name, phone, favorite, moment)) # Include favorite class and moment in INSERT statement
    db.commit()
    print(f'{num_contacts} test contacts added to the database.')
    db.close()

if __name__ == '__main__':
    generate_test_data(10)  # Generate 10 test contacts.
