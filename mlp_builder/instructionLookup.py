import xml.etree.ElementTree as ET

class InstructionLookup:
    def __init__(self):
        self.xml_source = '/home/kmacrae/gem5/mlp_builder/X86.xml'
        self.tree = ET.parse(self.xml_source)
        self.root = self.tree.getroot()
        self.instruction_lookup = {}
        for operation in self.root.find('one-byte'):
            opcode = operation.attrib['value']
            mnem = operation.find('entry').find('syntax').find('mnem')
            if mnem is not None:
                self.instruction_lookup[mnem.text.lower()] = int(opcode, 16)

    # When Provided an instrution's mnemonic it will convert it to the associated opcode
    def lookupInstruction(self, inst):
        opcode = None
        try:
            opcode = self.instruction_lookup[inst]
        except KeyError:
            opcode = -1
        return opcode
