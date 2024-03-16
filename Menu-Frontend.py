import argparse
from DatabaseAccess import DatabaseAccess

class MenuDrivenApp():
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="COMP3005 Postgresql CLI Application")
        subparsers = self.parser.add_subparsers(dest="command", help="Available commands")

        init_parser = subparsers.add_parser("init", help="Create table and populate it with initial data")

        addStudent_parser = subparsers.add_parser("addStudent", help="Add a student")
        addStudent_parser.add_argument("first_name", type=str, help="First name of the student")
        addStudent_parser.add_argument("last_name", type=str, help="Last name of the student")
        addStudent_parser.add_argument("email", type=str, help="Email of the student")
        addStudent_parser.add_argument("date", type=str, help="Enrollment date of the student")

        deleteStudent_parser = subparsers.add_parser("deleteStudent", help="Remove a student")
        deleteStudent_parser.add_argument("id", type=int, help="Student ID to remove")

        updateStudentEmail_parser = subparsers.add_parser("updateStudentEmail", help="Update a student's email")
        updateStudentEmail_parser.add_argument("id", type=int, help="Student ID to update")
        updateStudentEmail_parser.add_argument("new_email", type=str, help="New email of the student")

        getAllStudents_parser = subparsers.add_parser("getAllStudents", help="Get all students")

        # Connect to the local DB
        self.db = DatabaseAccess(conninfo='dbname=comp3005_a3 user=andrew', autocommit=True)


    def run(self):
        command_functions = {
            "init": self.initialize_table,
            "addStudent": self.addStudent,
            "deleteStudent": self.deleteStudent,
            "updateStudentEmail": self.updateStudentEmail,
            "getAllStudents": self.getAllStudents
        }
        self.print_help_menu()
        while True:
            command = input("Enter command (or 'q' or 'exit' to quit): ")
            if command in ['exit', 'q']:
                print("Exiting the program...")
                break
            if command in ['help', 'h']:
                self.print_help_menu()
                continue

            try:
                args = self.parser.parse_args(command.split())
            except SystemExit:
                '''
                    If the command is missing parameters, continue running main loop
                '''
                continue

            if args.command in command_functions:
                command_functions[args.command](args)
            else:
                print("Invalid command. Enter help or h for Available Commands")

    def print_help_menu(self):
        text: str = '''
                    Available commands:
                        init: Initialize the table with initial data
                        addStudent <FIRST_NAME>(str) <LAST_NAME>(str) <EMAIL>(str) <DATE>(YYYY-MM-DD):
                        deleteStudent <ID>(int)
                        updateStudentEmail <ID>(int) <NEW_EMAIL>(str)
                        getAllStudents: Get all students
                    '''
        print(text)

    def initialize_table(self, args):
        self.db.initialize_table()


    def deleteStudent(self, args):
        try:
            if self.db.deleteStudent(student_id=args.id):
                print(f"Student with ID {args.id} removed successfully.")
        except Exception as e:
            print(e)


    def addStudent(self, args):
        try:
            self.db.addStudent(first_name=args.first_name, last_name=args.last_name, email=args.email, date=args.date)
            print(f'Added Student with name: {args.first_name} {args.last_name} to the database.')
        except Exception as e:
            print(e)

    def updateStudentEmail(self, args):
        try:
            self.db.updateStudentEmail(student_id=args.id, new_email=args.new_email)
            print(f'Updated Student with ID: {args.id} email to {args.new_email}')
        except Exception as e:
            print(e)

    def getAllStudents(self, args):
        result: list[str] = self.db.getAllStudents()
        if not result:
            print(f"Could not get students.")
        else:
            print(f"Students: {result}")


if __name__ == "__main__":
    app = MenuDrivenApp()
    app.run()
