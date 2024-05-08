from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Database file path
DATABASE = '/nfs/demo.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row  # This enables name-based access to columns
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                favorite TEXT NOT NULL,
                moment TEXT NOT NULL
            );
        ''')
        db.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''  # Message indicating the result of the operation
    if request.method == 'POST':
        # Check if it's a delete action
        if request.form.get('action') == 'delete':
            contact_id = request.form.get('contact_id')
            db = get_db()
            db.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
            db.commit()
            message = 'Contact/Information deleted successfully.'
        else:
            name = request.form.get('name')
            phone = request.form.get('phone')
            favorite = request.form.get('favorite') # Get class from form
            moment = request.form.get('moment') # Get moment from form
            if name and phone and favorite:
                db = get_db()
                db.execute('INSERT INTO contacts (name, phone, favorite, moment) VALUES (?, ?, ?, ?)', (name, phone, favorite, moment)) #Insert class and moment into database
                db.commit()
                message = 'Contact/Information added successfully.'
            else:
                message = 'Missing name, phone number, class, or moment. Try again.' # Edited this message to include class

    # Always display the contacts table
    db = get_db()
    contacts = db.execute('SELECT * FROM contacts').fetchall()

    # Display the HTML form along with the contacts table
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Contact Information and Favorite Class/Moment</title>
        </head>
        <body>
            <h2>Add contact information, and say what your favorite class was that you have taken!</h2>
            <form method="POST" action="/">
                <label for="name">Name:</label><br>
                <input type="text" id="name" name="name" required><br>
                <label for="phone">Phone Number:</label><br>
                <input type="text" id="phone" name="phone" required><br><br>
                <label for="favorite">Class:</label><br>         <!-- Add class input field -->
                <input type="text" id="favorite" name="favorite" required><br><br>
                <label for="moment">Favorite Moment:</label><br>         <!-- Add moment input field -->
                <input type="text" id="moment" name="moment" required><br><br>
                <input type="submit" value="Submit">
            </form>
            <p>{{ message }}</p>
            {% if contacts %}
                <table border="1">
                    <tr>
                        <th>Name</th>
                        <th>Phone Number</th>
                        <th>Favorite Class</th>     <!-- Add column header for class -->
                        <th>Favorite Moment</th>     <!-- Add column header for moment -->
                        <th>Delete</th>
                    </tr>
                    {% for contact in contacts %}
                        <tr>
                            <td>{{ contact['name'] }}</td>
                            <td>{{ contact['phone'] }}</td>
                            <td>{{ contact['favorite'] }}</td>     <!-- Display class -->
                            <td>{{ contact['moment'] }}</td>     <!-- Display moment -->
                            <td>
                                <form method="POST" action="/">
                                    <input type="hidden" name="contact_id" value="{{ contact['id'] }}">
                                    <input type="hidden" name="action" value="delete">
                                    <input type="submit" value="Delete">
                                </form>
                            </td>
                        </tr>
                    {% endfor %}
                </table>
            {% else %}
                <p>No contacts found.</p>
            {% endif %}
        </body>
        </html>
    ''', message=message, contacts=contacts)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()  # Initialize the database and table
    app.run(debug=True, host='0.0.0.0', port=port)
