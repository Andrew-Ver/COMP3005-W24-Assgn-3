import argparse
from DatabaseAccess import DatabaseAccess
from prettytable import PrettyTable
from yaml import safe_load


class Menu():
    def __init__(self):
        '''
            Initialize the parser and subparsers
            to handle the commands and their arguments
        '''
        self.parser = argparse.ArgumentParser(description="COMP3005 Postgresql CLI Application")
        subparsers = self.parser.add_subparsers(dest="command", help="Available commands")

        init_parser = subparsers.add_parser("init", help="Create table and populate it with initial data")

        addStudent_parser = subparsers.add_parser("addstudent", help="Add a student -- addstudent <FIRST_NAME>(str) <LAST_NAME>(str) <EMAIL>(str) <DATE>(YYYY-MM-DD)")
        addStudent_parser.add_argument("first_name", type=str, help="First name of the student")
        addStudent_parser.add_argument("last_name", type=str, help="Last name of the student")
        addStudent_parser.add_argument("email", type=str, help="Email of the student")
        addStudent_parser.add_argument("date", type=str, help="Enrollment date of the student")

        deleteStudent_parser = subparsers.add_parser("deletestudent", help="Remove a student -- deletestudent <ID>(int)")
        deleteStudent_parser.add_argument("id", type=int, help="Student ID to remove")

        updateStudentEmail_parser = subparsers.add_parser("updatestudentemail", help="Update a student's email -- updatestudentemail <ID>(int) <NEW_EMAIL>(str)")
        updateStudentEmail_parser.add_argument("id", type=int, help="Student ID to update")
        updateStudentEmail_parser.add_argument("new_email", type=str, help="New email of the student")

        getAllStudents_parser = subparsers.add_parser("getallstudents", help="Get all students")

        # Set up the pretty table
        self.table = PrettyTable()
        self.table.field_names = ["ID", "First Name", "Last Name", "Email", "Enrollment Date"]

        # Connect to the local DB
        # Read the connection info from the config.yaml file
        try:
            with open('config.yaml', 'r') as file:
                conninfo = safe_load(file)
                # Fuse conninfo into a string
                conninfo = f"dbname={conninfo['dbname']} user={conninfo['user']} password={conninfo['password']}"
                self.db = DatabaseAccess(conninfo=conninfo, autocommit=True)
        except Exception as e:
            print(e)
            exit(1)

    def __del__(self):
        '''
            Close the connection to the database when the program exits
        '''
        self.db.close_conn()

    def run(self):
        '''
            Main loop of the program
            The program will continue to run until the user enters 'exit' or 'q'
        '''
        command_functions = {
            "init": self.initialize_table,
            "addstudent": self.addStudent,
            "deletestudent": self.deleteStudent,
            "updatestudentemail": self.updateStudentEmail,
            "getallstudents": self.getAllStudents
        }

        # On first run print the help menu
        self.print_help_menu()
        # # Initalize the table, removed this
        # self.initialize_table()

        while True:
            command = input("Enter command (or 'q' or 'exit' to quit): ").lower()
            if command in ['exit', 'q']:
                print("Exiting the program...")
                break
            if command in ['help', 'h']:
                self.print_help_menu()
                continue


            # Parse the command and its arguments
            try:
                args = self.parser.parse_args(command.split())
            except SystemExit:
                '''
                    If the command is missing parameters, continue running main loop
                '''
                continue

            # Execute the command with provided positional arguments
            if args.command in command_functions:
                command_functions[args.command](args)
            else:
                print("Invalid command. Enter help or h for Available Commands")

    def print_help_menu(self):
        text: str = '''
                    Available commands:
                        init: Initialize the table with initial data
                        addstudent <FIRST_NAME>(str) <LAST_NAME>(str) <EMAIL>(str) <DATE>(YYYY-MM-DD)
                        deletestudent <ID>(int)
                        updatestudentemail <ID>(int) <NEW_EMAIL>(str)
                        getallstudents: Get all students
                    '''
        print(text)

    def initialize_table(self, args=None):
        '''
            Initialize the table with initial data
            Also print the table after the initialization
        '''
        self.db.initialize_table()
        self.getAllStudents()


    def deleteStudent(self, args):
        '''
            Remove a student from the database by student_id
        '''
        try:
            if self.db.deleteStudent(student_id=args.id):
                print(f"Student with ID {args.id} removed successfully.")
        except Exception as e:
            print(e)


    def addStudent(self, args):
        '''
            Add a student to the database
        '''
        try:
            self.db.addStudent(first_name=args.first_name, last_name=args.last_name, email=args.email, date=args.date)
            print(f'Added Student with name: {args.first_name} {args.last_name} to the database.')
        except Exception as e:
            print(e)

    def updateStudentEmail(self, args):
        '''
            Update a student's email by student_id
        '''
        try:
            self.db.updateStudentEmail(student_id=args.id, new_email=args.new_email)
            print(f'Updated Student with ID: {args.id} email to {args.new_email}')
        except Exception as e:
            print(e)

    def getAllStudents(self, args=None):
        '''
            Get all students from the database,
            and pretty print the resulting db table
        '''
        try:
            result: list = self.db.getAllStudents()
            # Reset the table rows before adding and printing
            self.table.clear_rows()

            for row in result:
                self.table.add_row(row)

            print(self.table)

        except Exception as e:
            print(e)


if __name__ == "__main__":
    app = Menu()
    app.run()
