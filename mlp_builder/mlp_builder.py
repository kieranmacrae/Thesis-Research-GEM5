#!/usr/bin/env python2
from researchDB import ResearchDB
from instructionLookup import InstructionLookup
import pandas as pd
import argparse
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib

parser = argparse.ArgumentParser(description='Creates a neural network for a specified execution ID.')
parser.add_argument('-e', '--exec-id', dest='exec_id', type=int, help='An integer specifying an execution recoreded on the database.')
args = parser.parse_args()

# Modify here to change the layout of the neural network
# Be sure to rename the model, as this will become the name of the pickle file
clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(20))
name ="mpl_lbfgs_1e-5_20"

print "Creating a MLP from scikit learn..."

researchDB = ResearchDB()
instruction_lookup = InstructionLookup()

# Prepare the Training Data
print "Fetching branch data."
(X, y) = researchDB.getBranchData(args.exec_id)
print "Branch data collected."
X = X.applymap(instruction_lookup.lookupInstruction)
y = y.transpose()

print "Attempting to fit model."
clf.fit(X.values, y.values[0])

# Save the created MLP as a pickle file that can be imported elsewhere
joblib.dump(clf, name+'.pkl')

print "Finished! Pickle " + name + ".pkl has been created."
