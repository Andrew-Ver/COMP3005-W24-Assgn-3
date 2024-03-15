import psycopg

class DatabaseAccess:
    def __init__(self, conninfo: str, autocommit: bool=True) -> None:
        # Connect to a local database with the specified credentials
        # Autocommit enabled in order to not have to commit after any changes, saving code/errors
        try:
            self.conn = psycopg.connect(conninfo=conninfo, autocommit=autocommit)
            # Connection's cursor object to perform SQL operations with
            self.cur = self.conn.cursor()
        except Exception as e:
            print(f'Could not connect to database. {e}')

    def initalize_table(self) -> False:
        # Drop the table if it exists
        # And recreate the schema then populate with initial students
        try:
            self.cur.execute("""
                DROP TABLE IF EXISTS students;
                CREATE TABLE IF NOT EXISTS students (
                    student_id SERIAL PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    enrollment_date DATE NOT NULL
                );
                """)
            self.cur.execute("""
                INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
                    ('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
                    ('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
                    ('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02');
                            """)
        except Exception as e:
            print(f'Could not create table. {e}')
            self.conn.rollback()

    def drop_table(self) -> None:
        self.cur.execute('''
                        DROP TABLE IF EXISTS students;
                         ''')


    def addStudent(self, first_name: str, last_name: str, email: str, enrollment_date: str) -> bool:
        # Add student to the table
        try:
            self.cur.execute("""
                    INSERT INTO students (first_name, last_name, email, enrollment_date)
                            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(enrollment_date)s;
                    """,
                    {'first_name': first_name, 'last_name': last_name, 'email': email, 'enrollment_date': enrollment_date})
            return True
        except Exception as e:
            print(f'Could not add student. {e}')
            self.conn.rollback()
            return False

    def getAllStudents(self) -> list:
        try:
            result: list[str] = self.cur.execute("""
                            SELECT * FROM students;
                            """)
            return result.fetchall()
        except Exception as e:
            print(f'Could not get students. {e}')
            self.conn.rollback()
            return []

    def addStudent(self, first_name: str, last_name: str, email: str, enrollment_date: str) -> bool:
        try:
            self.cur.execute("""
                    INSERT INTO students (first_name, last_name, email, enrollment_date)
                             VALUES (%(first_name)s, %(last_name)s, %(email)s, %(enrollment_date)s);
                    """,
                    {'first_name': first_name, 'last_name': last_name, 'email': email, 'enrollment_date': enrollment_date})
            return True
        except Exception as e:
            print(f'Could not add student. {e}')
            self.conn.rollback()
            return False

    def updateStudentEmail(self, student_id: int, new_email: str) -> bool:
        try:
            self.cur.execute("""
                    UPDATE students
                    SET email = %(new_email)s
                    WHERE student_id = %(student_id)s;
                    """,
                    {'new_email': new_email, 'student_id': student_id})
            return True
        except Exception as e:
            print(f'Could not update student id {id} email. {e}')
            self.conn.rollback()
            return False

    def deleteStudent(self, student_id: int) -> bool:
        try:
            self.cur.execute("""
                            DELETE FROM students
                            WHERE student_id = %(student_id)s;
                            """,
                            {'student_id': student_id})
            return True
        except Exception as e:
            print(f'Could not delete student with ID: {student_id}. {e}')
            self.conn.rollback()
            return False

    def close_conn(self) -> None:
        # Close the cursor and database connection
        self.cur.close()
        self.conn.close()
