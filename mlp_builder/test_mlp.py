#!/usr/bin/env python2
from researchDB import ResearchDB
from instructionLookup import InstructionLookup

import argparse
import pandas as pd
from sklearn.externals import joblib
from sklearn.neural_network import MLPClassifier

# Load the specified MLP Pickle and the execution id from the command line parameters
parser = argparse.ArgumentParser(description="Tests a specified mlp with execution deata froma  specified execution.")
parser.add_argument('-m', '--mlp-file-name', dest='mlp_name', help='Filename for the saved MLP Pickle.')
parser.add_argument('-e', '--exec-id', dest='exec_id', type=int, help='The execution ID that should be loaded for testing.')
args = parser.parse_args()
mlp_name = args.mlp_name
exec_id = args.exec_id

# Load the Pickle
clf = joblib.load(mlp_name)
print "MLP Pickle successfully loaded."

# Load the test data
print "Loading test data for exececution: "+ str(exec_id)
researchDB = ResearchDB()
instruction_lookup = InstructionLookup()

(X, y) = researchDB.getBranchData(exec_id)
X = X.applymap(instruction_lookup.lookupInstruction)

num_correct   = 0
num_incorrect = 0

for i in range(0, X.shape[0]):
    predicted = clf.predict(pd.DataFrame(X.iloc[i]).transpose())[0]
    expected = y.iloc[0].values[0]
    if predicted == expected:
        num_correct += 1
    else:
        num_incorrect += 1

print "Total correct predictions:   " + str(num_correct)
print "Total incorrect predictions: " + str(num_incorrect)
print "Missprediction rate is: " + str(num_incorrect / float(num_correct + num_incorrect) * 100)  + "%"
