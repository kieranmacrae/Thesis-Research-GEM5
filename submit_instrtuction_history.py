import psycopg2
import sys

class Database:
    def __init__(self):
        connection_string = "dbname='research' user='gem5' password='gem5' host='192.168.1.22'"
        self.connection = psycopg2.connect(connection_string)
        self.cursor = self.connection.cursor()

    def addProgramExecution(self, program_name, program_parameters=None):
        try:
            self.cursor.execute("""INSERT INTO program_execution (program_name, program_parameters) VALUES (%s, %s);""", (program_name, program_parameters))
            self.cursor.execute("""SELECT currval(pg_get_serial_sequence('program_execution', 'execution_id'));""")
            exec_id = self.cursor.fetchone()
            self.connection.commit()
            return(exec_id[0])
        except psycopg2.Error as error:
            print(error)

    def recordBranchOutcome(self, exec_id, branch_outcome, instruction_history):
        try:
            self.cursor.execute("""INSERT INTO branch_history (execution_id, branch_outcome) VALUES ({}, {});""".format(exec_id, branch_outcome))
            self.cursor.execute("""SELECT currval(pg_get_serial_sequence('branch_history', 'branch_id'));""")
            branch_id = self.cursor.fetchone()[0]
            for instruction in instruction_history:
                self.cursor.execute("""INSERT INTO instruction_history (execution_id, branch_id, instruction) VALUES ({}, {}, '{}');""".format(exec_id, branch_id, instruction))
            self.connection.commit()
        except psycopg2.Error as error:
            print(error)

def parseBranchOutcome(line):
        head, *tail = line.split()
        return (bool(int(head)), tail)
 
# The basic process of submitting the files to the database
def main():
    print('Submitting instruction history and branch outcomes to the database.')
    arguments = sys.argv[1:]
    program_params = None
    if len(arguments) < 1:
        print("You must specify the executed program")
        return
    if len(arguments) == 2:
        program_params = arguments[1]
    # Insert a new entry into the program_execution table
    database = Database()
    exec_id = database.addProgramExecution(arguments[0])
    with open("branch_history.txt") as file_handle:
        for index, line in enumerate(file_handle):
            (branch_outcome, instruction_history) = parseBranchOutcome(line)
            if instruction_history:
                database.recordBranchOutcome(exec_id, branch_outcome, instruction_history)
            if (index % 1000) == 0:
                print("Submitted {} branches.".format(index))

# Run the main function when the program is called
if __name__ == "__main__":
    main()
