import psycopg2 as ps
import pandas as pd
import datetime

class ResearchDB:
    def __init__(self):
        self.connect_str = "dbname='research' user='jupyter' host='192.168.1.22' password='jupyter'"
        self.connection = ps.connect(self.connect_str)
        self.cursor = self.connection.cursor()

    # For a given execution ID retrieve all the branch outcomes and the associated instructions leading to this outcome
    def getBranchData(self, exec_id):
        self.cursor.execute("""SELECT branch_id, branch_outcome FROM branch_history WHERE execution_id={};""".format(exec_id))
        branch_data = pd.DataFrame(self.cursor.fetchall())
        branch_outcomes = pd.DataFrame(branch_data[1])
        instruction_history = pd.DataFrame()
        results = []
        counter = 0;
        start_time = datetime.datetime.now()
        current_time = start_time
        for index, branch_id in enumerate(branch_data[0]):
            self.cursor.execute("""SELECT instruction FROM instruction_history WHERE execution_id={} AND branch_id={} LIMIT 20;""".format(exec_id, branch_id))
            df = pd.DataFrame(self.cursor.fetchall())
            results.append(df.transpose())
            counter += 1
            if (counter == len(branch_data[0])/100):
                counter = 0
                prev_time = current_time
                current_time = datetime.datetime.now()
                difference = current_time - prev_time
                print "Completed: " + str(index) + "/" + str(len(branch_data[0])) + ". Took: " + str(difference.seconds) + " seconds."
        current_time = datetime.datetime.now()
        difference = current_time - start_time
        print "All registers fetched. Took " + str(difference.seconds) + "s." 
        print "Attempting to concatenate..."
        instruction_history = pd.concat(results)
        concat_time = datetime.datetime.now()
        difference = concat_time - current_time
        print "Concatenation completed. Took " + str(difference.seconds) + "s."
        return (instruction_history, branch_outcomes)
