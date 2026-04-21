# 🎓 Student Management System

A full-stack CRUD web application built with **HTML/CSS/JavaScript**, **Python Flask**, and **MySQL** — designed as a placement interview project.

---

## 📸 Features

- ➕ **Add** new students
- 📋 **View** all students in a table
- ✏️ **Edit** student details
- 🗑️ **Delete** students
- 📊 Live stats (total students, courses)
- ✅ Form validation
- 🔒 SQL Injection protection

---

## 🛠️ Tech Stack

| Layer      | Technology                  |
|------------|-----------------------------|
| Frontend   | HTML, CSS, JavaScript       |
| Backend    | Python 3, Flask             |
| Database   | MySQL                       |
| Libraries  | flask-cors, mysql-connector |

---

## 📁 Folder Structure

```
student_management/
│
├── app.py                  ← Flask backend (API + routes)
├── database_setup.sql      ← MySQL database & table setup
├── requirements.txt        ← Python dependencies
├── README.md               ← You are here
│
└── templates/              ← Flask looks for HTML here (important!)
    └── index.html          ← Frontend (HTML + CSS + JS)
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.x installed
- MySQL installed and running
- pip (Python package manager)

---

### Step 1 — Clone / Download the project

```bash
cd C:\Users\yourname\
# Place the project folder here
```

---

### Step 2 — Install Python dependencies

```bash
pip install flask flask-cors mysql-connector-python
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

---

### Step 3 — Set up the MySQL database

Open your MySQL terminal and run:

```bash
mysql -u root -p < database_setup.sql
```

Or manually copy-paste the commands from `database_setup.sql` into MySQL Workbench / terminal.

This will:
- Create a database called `student_db`
- Create the `students` table
- Insert 5 sample students

---

### Step 4 — Update your database password

Open `app.py` and find this section:

```python
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",   # ← Change this to YOUR MySQL password
        database="student_db"
    )
```

---

### Step 5 — Run the Flask server

```bash
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

---

### Step 6 — Open in browser

Visit: **http://localhost:5000**

---

## 🌐 API Endpoints

| Operation    | Method | Endpoint          | Request Body                                      |
|-------------|--------|-------------------|---------------------------------------------------|
| Add student  | POST   | `/students`       | `{"name":"Rahul","age":20,"course":"CSE","email":"..."}` |
| Get all      | GET    | `/students`       | —                                                 |
| Get one      | GET    | `/students/<id>`  | —                                                 |
| Update       | PUT    | `/students/<id>`  | `{"name":"Rahul","age":21,"course":"CSE","email":"..."}` |
| Delete       | DELETE | `/students/<id>`  | —                                                 |

---

## 🐛 Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `TemplateNotFound: index.html` | `index.html` not inside `templates/` folder | Create a `templates/` folder next to `app.py` and move `index.html` inside it |
| `Access denied for user 'root'` | Wrong MySQL password | Update `password=` in `app.py` |
| `No module named 'flask'` | Flask not installed | Run `pip install flask flask-cors mysql-connector-python` |
| `Failed to fetch` in browser | Flask server not running | Run `python app.py` first |
| `1062 Duplicate entry` | Email already exists in DB | Use a unique email address |

---

## 🗄️ Database Schema

```sql
CREATE TABLE students (
    id      INT AUTO_INCREMENT PRIMARY KEY,
    name    VARCHAR(100) NOT NULL,
    age     INT NOT NULL,
    course  VARCHAR(50)  NOT NULL,
    email   VARCHAR(100) NOT NULL UNIQUE
);
```

---

## 📊 How Data Flows

```
User fills form → JavaScript collects data
      ↓
fetch() sends POST/PUT/DELETE request to Flask
      ↓
Flask receives request → runs SQL query
      ↓
MySQL saves/updates/deletes data
      ↓
Flask sends JSON response back
      ↓
JavaScript updates the table on screen
```

---

## 👨‍💻 Author




---

## 📄 License

This project is open-source and free to use for learning purposes.
