"""
============================================================
  STUDENT MANAGEMENT SYSTEM - Flask Backend
  Author: Interview Prep Guide
  Tech Stack: Python (Flask) + MySQL
============================================================

WHAT IS THIS FILE?
------------------
This is the BRAIN of our web application.
Flask is a Python web framework - it listens for requests
from the browser and sends back responses.

Think of Flask like a WAITER in a restaurant:
- Browser (customer) makes a request (order)
- Flask (waiter) takes the request
- MySQL (kitchen) processes and stores data (cooks food)
- Flask sends the result back (delivers food)
"""

# ============================================================
# STEP 1: IMPORT LIBRARIES
# ============================================================

from flask import Flask, request, jsonify, render_template
# Flask       → The web framework itself
# request     → Helps us READ data sent from the browser (form data, JSON)
# jsonify     → Converts Python dictionaries into JSON format for browser
# render_template → Sends HTML files to the browser

from flask_cors import CORS
# CORS = Cross-Origin Resource Sharing
# Without this, browser BLOCKS requests from frontend to backend
# Think of it as "permission slip" to allow communication

import mysql.connector
# This is the MySQL driver - it lets Python TALK to MySQL database
# Like a translator between Python and MySQL

# ============================================================
# STEP 2: CREATE THE FLASK APP
# ============================================================

app = Flask(__name__)
# Flask(__name__) creates our web application
# __name__ tells Flask where to look for template files

CORS(app)
# Enable CORS for all routes - allows browser to make API calls

# ============================================================
# STEP 3: DATABASE CONNECTION FUNCTION
# ============================================================

def get_db_connection():
    """
    WHY A FUNCTION?
    ---------------
    We need database connection in every CRUD operation.
    Instead of writing connection code 4 times, we write it ONCE
    in a function and call it wherever needed.
    This is called DRY principle → Don't Repeat Yourself

    WHAT HAPPENS INTERNALLY?
    ------------------------
    Python sends a "connection request" to MySQL server.
    MySQL checks username & password.
    If correct, MySQL opens a "channel" for communication.
    We call this channel a "connection object".
    """
    connection = mysql.connector.connect(
        host="localhost",       # Where MySQL is running (our own computer)
        user="root",            # MySQL username (change if different)
        password="your_password",  # MySQL password (change this!)
        database="student_db"  # Which database to use
    )
    return connection
    # We RETURN the connection so the calling function can use it


# ============================================================
# STEP 4: ROUTE - SERVE HTML PAGE
# ============================================================

@app.route('/')
def index():
    """
    WHAT IS A ROUTE?
    ----------------
    A route is a URL pattern. When user visits '/', Flask
    runs this function and returns whatever it returns.

    @app.route('/') is called a DECORATOR.
    It tells Flask: "When someone visits the homepage (/),
    run the index() function below."

    render_template('index.html') sends our HTML file to browser.
    Flask looks for HTML files in a folder called 'templates/'
    """
    return render_template('index.html')


# ============================================================
# STEP 5: CREATE - Add a new student (POST /students)
# ============================================================

@app.route('/students', methods=['POST'])
def add_student():
    """
    URL: POST /students
    PURPOSE: Add a new student to the database

    WHY POST?
    ---------
    HTTP has different "methods" (verbs):
    - GET    → "Give me data" (reading)
    - POST   → "Here is new data, save it" (creating)
    - PUT    → "Update existing data" (updating)
    - DELETE → "Remove this data" (deleting)

    WHAT HAPPENS STEP BY STEP:
    --------------------------
    1. Browser sends student data (name, age, etc.) to this URL
    2. Flask receives it in request.json
    3. We extract each field
    4. We connect to database
    5. We run SQL INSERT command
    6. We send back a success message
    """

    # Step A: Get the data sent from browser
    data = request.json
    # request.json reads the JSON body sent by the browser
    # Example: {"name": "Rahul", "age": 20, "course": "CSE", "email": "rahul@email.com"}

    # Step B: Extract individual fields from the data
    name = data['name']      # Student's name
    age = data['age']        # Student's age
    course = data['course']  # Student's course (CSE, ECE, etc.)
    email = data['email']    # Student's email

    # Step C: Connect to database
    conn = get_db_connection()
    # conn is now our "open channel" to MySQL

    cursor = conn.cursor()
    # cursor is like a "pen" that writes SQL commands to MySQL
    # Without cursor, we can't execute SQL queries

    # Step D: Write and execute SQL query
    query = "INSERT INTO students (name, age, course, email) VALUES (%s, %s, %s, %s)"
    values = (name, age, course, email)
    # 
    # WHY %s INSTEAD OF WRITING VALUES DIRECTLY?
    # -------------------------------------------
    # WRONG way:  "INSERT INTO students VALUES ('" + name + "'...)"
    # This causes SQL INJECTION - a serious security attack!
    # 
    # RIGHT way: Use %s as placeholder, pass values separately.
    # MySQL driver automatically "sanitizes" (cleans) the values.
    # This is called a PARAMETERIZED QUERY or PREPARED STATEMENT.

    cursor.execute(query, values)
    # cursor.execute() sends the SQL command to MySQL
    # MySQL finds the students table and inserts a new row

    conn.commit()
    # VERY IMPORTANT! Without commit(), changes are NOT saved permanently.
    # Think of commit() like "Ctrl+S" (Save) in a text editor.
    # MySQL keeps changes in temporary memory until commit() is called.

    # Step E: Close connections (free up resources)
    cursor.close()
    conn.close()
    # Always close cursor and connection after use.
    # Like turning off tap after use - saves resources.

    # Step F: Send success response back to browser
    return jsonify({"message": "Student added successfully!"}), 201
    # jsonify() converts Python dict to JSON format
    # 201 is HTTP status code meaning "Created successfully"
    # Common HTTP codes:
    # 200 = OK (general success)
    # 201 = Created (new resource created)
    # 400 = Bad Request (client sent wrong data)
    # 404 = Not Found
    # 500 = Server Error


# ============================================================
# STEP 6: READ - Get all students (GET /students)
# ============================================================

@app.route('/students', methods=['GET'])
def get_students():
    """
    URL: GET /students
    PURPOSE: Fetch ALL students from the database

    WHAT HAPPENS INTERNALLY:
    ------------------------
    1. Browser requests this URL
    2. Flask connects to MySQL
    3. SQL SELECT query runs - MySQL scans the table
    4. MySQL returns all matching rows
    5. We convert rows to list of dictionaries
    6. We send it back as JSON to the browser
    7. Browser's JavaScript displays it in a table
    """

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # dictionary=True → Each row comes as a Python DICTIONARY
    # Without it: row = (1, "Rahul", 20, "CSE", "rahul@email.com")  ← tuple
    # With it:    row = {"id": 1, "name": "Rahul", "age": 20, ...}  ← dict
    # Dictionary is easier to work with and convert to JSON

    cursor.execute("SELECT * FROM students")
    # SELECT * → Select ALL columns
    # FROM students → From the students table
    # No WHERE clause → Return ALL rows

    students = cursor.fetchall()
    # fetchall() → Gets ALL rows returned by the query
    # Other options:
    # fetchone()  → Gets only the FIRST row
    # fetchmany(5) → Gets only 5 rows

    cursor.close()
    conn.close()

    return jsonify(students)
    # jsonify converts the list of dicts to JSON array
    # Example output:
    # [
    #   {"id": 1, "name": "Rahul", "age": 20, ...},
    #   {"id": 2, "name": "Priya", "age": 21, ...}
    # ]


# ============================================================
# STEP 7: UPDATE - Update student details (PUT /students/<id>)
# ============================================================

@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    """
    URL: PUT /students/1  (where 1 is the student ID)
    PURPOSE: Update an existing student's information

    WHAT IS <int:id>?
    -----------------
    <int:id> is a URL PARAMETER (also called route variable).
    It captures whatever number is in the URL.
    
    If URL is /students/5  → id = 5
    If URL is /students/10 → id = 10
    
    Flask automatically passes it as a function argument: update_student(id)
    
    int: means Flask converts it to integer automatically.
    Without int:, it would be a string "5" instead of number 5.

    SQL UPDATE EXPLANATION:
    -----------------------
    UPDATE students          → Target the students table
    SET name=%s, age=%s, ... → Change these columns to new values
    WHERE id=%s             → Only update the row with this specific id
    
    WHY WHERE CLAUSE IS CRITICAL:
    Without WHERE → ALL students get updated! (disaster!)
    With WHERE id=5 → Only student with id=5 gets updated (correct!)
    """

    data = request.json
    name = data['name']
    age = data['age']
    course = data['course']
    email = data['email']

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "UPDATE students SET name=%s, age=%s, course=%s, email=%s WHERE id=%s"
    values = (name, age, course, email, id)
    # Notice: id goes at the END because it corresponds to the last %s (WHERE id=%s)
    # Order of values must match order of %s placeholders

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Student updated successfully!"})


# ============================================================
# STEP 8: DELETE - Remove a student (DELETE /students/<id>)
# ============================================================

@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    """
    URL: DELETE /students/3  (where 3 is the student ID)
    PURPOSE: Delete a student record permanently

    SQL DELETE EXPLANATION:
    -----------------------
    DELETE FROM students → Remove row(s) from students table
    WHERE id=%s          → Only delete the row with this specific id
    
    WARNING: DELETE without WHERE deletes ALL data in the table!
    Always use WHERE clause in DELETE queries.
    
    REAL-WORLD ANALOGY:
    Think of DELETE as tearing a specific page from a notebook.
    WHERE id=3 means "tear only page number 3".
    Without WHERE, you'd tear ALL pages (empty notebook!).
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM students WHERE id = %s"
    cursor.execute(query, (id,))
    # Note: (id,) with a trailing comma creates a TUPLE with one element
    # mysql.connector requires values as tuple, not single value
    # (id,) is correct ✓
    # (id) is just parentheses, not a tuple ✗

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Student deleted successfully!"})


# ============================================================
# STEP 9: GET SINGLE STUDENT - For Edit Form
# ============================================================

@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    """
    URL: GET /students/3
    PURPOSE: Fetch ONE specific student (used when editing)
    
    When user clicks "Edit" button, we need to pre-fill the form
    with that student's current data. This endpoint fetches it.
    """

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
    student = cursor.fetchone()
    # fetchone() gets only the FIRST matching row
    # Since id is unique (PRIMARY KEY), there's only one match

    cursor.close()
    conn.close()

    if student:
        return jsonify(student)
    else:
        return jsonify({"error": "Student not found"}), 404
    # If no student found with that id, return 404 Not Found


# ============================================================
# STEP 10: RUN THE APP
# ============================================================

if __name__ == '__main__':
    """
    WHAT IS if __name__ == '__main__'?
    -----------------------------------
    When Python runs a file directly (python app.py), 
    __name__ is set to '__main__'.
    
    When a file is imported by another file,
    __name__ is set to the filename.
    
    So this block only runs when WE run app.py directly.
    It PREVENTS the server from starting when imported as a module.
    
    debug=True means:
    - Flask shows detailed error messages
    - Flask automatically restarts when you save code changes
    - NEVER use debug=True in production (security risk!)
    
    port=5000 means:
    - The app runs on http://localhost:5000
    - 5000 is Flask's default port
    """
    app.run(debug=True, port=5000)
