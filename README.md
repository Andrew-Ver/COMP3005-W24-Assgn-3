# COMP3005 Assignment 3 Winter 2024

### Setup
Make sure Python is installed and install the pip dependencies with ```pip install requirements.txt```, optionally creating a virtual environment.

**Ensure Postgresql server is running locally and a database to connect to is created.**

## YouTube Demo Link
**https://youtu.be/e6YbQGMp5RI**

### Project Structure
---
* ```setup/setup.sql```
  * Sets up the database, creates 'students' table, and populates it with initial data
* ```DatabaseAccess.py```
  * A database access layer for PostgreSQL DB using Psycopg library
* ```config.yaml```
  * Contains configuration (conninfo) data for the database access layer to consume
* ```Menu-Frontend.py```
  * The CLI, menu-driven frontend for accessing the application by the user

## Setup Instructions

* ### Ensure *local PostgreSQL server* is running and The Database is setup with proper permissions
* ### (Optional) Run the database and table set up script ```setup.sql```

* ### Modify ```config.yaml```
    * Change the database name, database user, and any other connection parameters to ```config.yaml```

## Frontend Interaction
* Proceed to run with ```python3 Menu-Frontend.py``` from terminal
* Each command takes *positional arguments*, and all arguments are ***required***:

| Command            | Purpose                                              | Arguments                                                                   |
|--------------------|------------------------------------------------------|-----------------------------------------------------------------------------|
| **init**              | *initialize the table with default* data               |                                                                             |
| **addstudent**        | *add a new student to the  students table*             | <FIRST_NAME>(str)  <LAST_NAME> (str)  <EMAIL\>(str)      <DATE\>(YYYY-MM-DD) |
| **deletestudent**      | delete a student from the students table by their id | <ID\>        (int)                                                           |
| **updatestudentemail** | *update a student's email*                             | <ID\>        (int) <NEW_EMAIL> (str)                                         |
| **getallstudents**     | *print every row in the  students table*               |                                                                             |
