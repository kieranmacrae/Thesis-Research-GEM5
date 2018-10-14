from instructionLookup import InstructionLookup
from sklearn.externals import joblib
from sklearn.neural_network import MLPClassifier

# Class defines the interface for the Instruction History predictor.
# Must initialize with the fully qualified 
# filename of the desired MLP predictor.
class InstructionPredictor:

    def __init__(self, mlp_name):
        self.predictor = joblib.load(mlp_name)
        self.instruction_lookup = InstructionLookup()
        self.instruction_history = []

    # When provided with an array of 20 instructions 
    # will use the predictor to produce an outcome.
    def predict(self, instructions):
        converted_instructions = [
                self.instruction_lookup.lookupInstruction(inst) for inst in instructions]
        return self.predictor.predict([converted_instructions])[0]


def checkFile(i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, 
        i11, i12, i13, i14, i15, i16, i17, i18, i19, i20):
    # Initializse the instruction history predictor
    instruction_predictor = InstructionPredictor(
            "/home/kmacrae/gem5/mlp_builder/mlps/mpl_lbfgs_1e-5_10.pkl")

    # Need to get the instructions into array form.
    instructions = [i1, i2, i3, i4, i5, i6, i7, i8, i9, i10,
            i11, i12, i13, i14, i15, i16, i17, i18, i19, i20]
    
    return instruction_predictor.predict(instructions)

