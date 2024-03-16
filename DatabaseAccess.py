import psycopg


class DatabaseAccess:
    def __init__(self, conninfo: str, autocommit: bool=True) -> None:
        try:
            # Connect to a local database with the specified credentials
            # Autocommit enabled in order to not have to commit after any changes, saving code/errors
            self.conn = psycopg.connect(conninfo=conninfo, autocommit=autocommit)
            # Connection's cursor object to perform SQL operations with
            self.cur = self.conn.cursor()
        except Exception as e:
            raise Exception(f'Could not connect to the database, please double-check conninfo. {e}')

    def initialize_table(self) -> None:
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
            self.conn.rollback()
            raise Exception(f'Could not initialize table. {e}')

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
            self.conn.rollback()
            raise Exception(f'Could not add student. {e}')

    def getAllStudents(self) -> list:
        try:
            result: list[str] = self.cur.execute("""
                            SELECT * FROM students;
                            """)
            return result.fetchall()
        except Exception as e:
            self.conn.rollback()
            raise Exception(f'Could not get students. {e}')

    def addStudent(self, first_name: str, last_name: str, email: str, date: str) -> bool:
        try:
            self.cur.execute("""
                    INSERT INTO students (first_name, last_name, email, enrollment_date)
                             VALUES (%(first_name)s, %(last_name)s, %(email)s, %(enrollment_date)s);
                    """,
                    {'first_name': first_name, 'last_name': last_name, 'email': email, 'enrollment_date': date})
            return True
        except Exception as e:
            self.conn.rollback()
            raise Exception(f'Could not add student. {e}')

    def updateStudentEmail(self, student_id: int, new_email: str) -> bool:
        try:
            self.cur.execute("""
                    UPDATE students
                    SET email = %(new_email)s
                    WHERE student_id = %(student_id)s;
                    """,
                    {'new_email': new_email, 'student_id': student_id})
            if self.cur.rowcount == 0:
                self.conn.rollback()
                raise Exception('Student ID doesn\'t exist.')
            return True
        except Exception as e:
            self.conn.rollback()
            raise Exception(f'Could not update student id {student_id} email. {e}')

    def deleteStudent(self, student_id: int) -> bool:
        try:
            self.cur.execute("""
                            DELETE FROM students
                            WHERE student_id = %(student_id)s;
                            """,
                            {'student_id': student_id})
            # student_id does not exist in the table
            if self.cur.rowcount == 0:
                raise Exception('Student ID doesn\'t exist.')
            return True
        except Exception as e:
            self.conn.rollback()
            raise Exception(f'Could not delete student with ID: {student_id}. {e}')

    # Get a student by their ID
    # Just for testing...
    def getStudent(self, student_id: int) -> list:
        try:
            result: list[str] = self.cur.execute("""
                            SELECT * FROM students
                            WHERE student_id = %(student_id)s;
                            """,
                            {'student_id': student_id})
            return result.fetchone()
        except Exception as e:
            print(f'Could not get student with ID: {student_id}. {e}')
            self.conn.rollback()
            return None

    def close_conn(self) -> None:
        # Close the cursor and database connection
        self.cur.close()
        self.conn.close()