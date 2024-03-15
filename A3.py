from DatabaseAccess import DatabaseAccess

config: str = {
    'dbname': 'comp3005_a3',
    'user': 'andrew',
}
# Merge the config dictionary into a string to be consumed by the DatabaseAccess object
config_str = ' '.join(f'{k}={v}' for k, v in config.items() if v != 'None' and v != '')

# Create a new DatabaseAccess object with the specified connection info
db = DatabaseAccess(conninfo=config_str, autocommit=True)

db.initalize_table()


for student in db.getAllStudents():
    print(student)

print('\n')


db.addStudent('John', 'Doe', 'john@doe.com', '2023-09-01')

for student in db.getAllStudents():
    print(student)

# Close the connection to the database at the end
db.close_conn()
