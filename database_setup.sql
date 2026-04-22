-- ============================================================
--  STUDENT MANAGEMENT SYSTEM - Database Setup
--  Run this file in MySQL to set up your database
--  Command: mysql -u root -p < database_setup.sql
-- ============================================================

-- ──────────────────────────────────────────────────────────
-- STEP 1: CREATE THE DATABASE
-- ──────────────────────────────────────────────────────────

CREATE DATABASE IF NOT EXISTS student_db;
-- CREATE DATABASE → Creates a new database (a container for tables)
-- IF NOT EXISTS   → Only creates if it doesn't already exist
--                   Without this, running the script twice would cause an ERROR

-- ──────────────────────────────────────────────────────────
-- STEP 2: SELECT THE DATABASE TO USE
-- ──────────────────────────────────────────────────────────

USE student_db;
-- Tells MySQL: "All following commands should run in student_db"
-- Without this, MySQL doesn't know WHICH database to create the table in

-- ──────────────────────────────────────────────────────────
-- STEP 3: CREATE THE STUDENTS TABLE
-- ──────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS students (

    id      INT AUTO_INCREMENT PRIMARY KEY,
    -- id          → Column name
    -- INT         → Data type: stores whole numbers (1, 2, 3...)
    -- AUTO_INCREMENT → MySQL automatically assigns next number (1, 2, 3...)
    --               You don't need to provide this value when inserting
    -- PRIMARY KEY → Uniquely identifies each row
    --               No two students can have same id
    --               Cannot be NULL (empty)
    
    name    VARCHAR(100) NOT NULL,
    -- VARCHAR(100) → Variable-length text, max 100 characters
    --               "Variable" means it only uses space it needs
    --               "Rahul" uses 5 bytes, not 100 bytes
    -- NOT NULL     → This field MUST have a value (cannot be empty)
    
    age     INT NOT NULL,
    -- INT          → Whole number for age (20, 21, 22...)
    
    course  VARCHAR(50) NOT NULL,
    -- VARCHAR(50)  → Course name (max 50 characters)
    
    email   VARCHAR(100) NOT NULL UNIQUE
    -- UNIQUE       → No two students can have same email address
    --               MySQL will REJECT insert if email already exists
    --               Prevents duplicate registrations
);

-- ──────────────────────────────────────────────────────────
-- WHAT DOES OUR TABLE LOOK LIKE?
-- ──────────────────────────────────────────────────────────

-- After creating the table, it's an empty grid:
-- 
-- +----+------+-----+--------+-------+
-- | id | name | age | course | email |
-- +----+------+-----+--------+-------+
-- (empty - no rows yet)
-- +----+------+-----+--------+-------+


-- ──────────────────────────────────────────────────────────
-- STEP 4: INSERT SAMPLE DATA (for testing)
-- ──────────────────────────────────────────────────────────

INSERT INTO students (name, age, course, email) VALUES
    ('Rahul Kumar',  20, 'B.Tech CSE', 'rahul.kumar@email.com'),
    ('Priya Sharma', 21, 'B.Tech ECE', 'priya.sharma@email.com'),
    ('Amit Singh',   22, 'MCA',        'amit.singh@email.com'),
    ('Sneha Reddy',  20, 'BCA',        'sneha.reddy@email.com'),
    ('Arjun Rao',    23, 'MBA',        'arjun.rao@email.com');

-- Note: We do NOT provide 'id' values
-- AUTO_INCREMENT handles that automatically!
-- MySQL will assign id = 1, 2, 3, 4, 5

-- ──────────────────────────────────────────────────────────
-- STEP 5: VERIFY THE DATA
-- ──────────────────────────────────────────────────────────

SELECT * FROM students;
-- SELECT *    → Select ALL columns
-- FROM students → From the students table
-- (no WHERE)  → Return ALL rows
-- 
-- Expected output:
-- +----+---------------+-----+------------+------------------------+
-- | id | name          | age | course     | email                  |
-- +----+---------------+-----+------------+------------------------+
-- |  1 | Rahul Kumar   |  20 | B.Tech CSE | rahul.kumar@email.com  |
-- |  2 | Priya Sharma  |  21 | B.Tech ECE | priya.sharma@email.com |
-- |  3 | Amit Singh    |  22 | MCA        | amit.singh@email.com   |
-- |  4 | Sneha Reddy   |  20 | BCA        | sneha.reddy@email.com  |
-- |  5 | Arjun Rao     |  23 | MBA        | arjun.rao@email.com    |
-- +----+---------------+-----+------------+------------------------+


-- ──────────────────────────────────────────────────────────
-- USEFUL SQL COMMANDS (for reference/practice)
-- ──────────────────────────────────────────────────────────

-- View table structure:
-- DESCRIBE students;

-- Count total students:
-- SELECT COUNT(*) FROM students;

-- Find students by course:
-- SELECT * FROM students WHERE course = 'B.Tech CSE';

-- Find students above age 21:
-- SELECT * FROM students WHERE age > 21;

-- Delete all sample data (if needed):
-- DELETE FROM students;

-- Drop (delete) the entire table:
-- DROP TABLE students;

-- Drop (delete) the entire database:
-- DROP DATABASE student_db;
