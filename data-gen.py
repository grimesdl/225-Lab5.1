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
    db.execute('''ALTER TABLE contacts ADD COLUMN favclass TEXT''')
    db.commit()
    
    for i in range(num_contacts):
        name = f'Test Name {i}'
        phone = f'123-456-789{i}'
        favclass = f'My favorite class was CIT225{i}' # Add favorite class
        db.execute('INSERT INTO contacts (name, phone, favclass) VALUES (?, ?, ?)', (name, phone, favclass)) # Include favorite class in INSERT statement
    db.commit()
    print(f'{num_contacts} test contacts added to the database.')
    db.close()

if __name__ == '__main__':
    generate_test_data(10)  # Generate 10 test contacts.
