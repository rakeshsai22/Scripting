class Gate:
    # inlcudes all the gate info: name(NAND,AND), fani_in and fan_out, delay and slew info
    def __init__(self,gate_id,gate_type):
        self.gate_id=gate_id
        self.gate_type=gate_type
        self.fanin=[]
        self.fanout=[]
        self.delay=None
        self.slew=None
        self.arriv_time = 0 # will be fetched from the lib

        def add_fanin(self,gate):
            self.fanin.append(gate)
        
        def add_fanout(self,gate):
            self.fanout.append(gate)

class Circuit:
    # contains all the ckt details: inputs,outputs,gates
    def __init__(self):
        self.inputs =[]
        self.outputs =[]
        self.gates = {}


    def add_input(self, input_id):
        self.inputs.append(input_id)

    def add_output(self,output_id):
        self.outputs.append(output_id)

    def add_gate(self,gate):
        self.gates[gate.gate_id] = gate

#  Netlist parsing

def parse_netlist(filename):
    circuit = Circuit()

    with open(filename,'r') as file:
        for line in file:
            line = line.strip()
            if line.startwith("INPUT"):
                input_id = line[line.find("(")+1:line.find(")")]
                circuit.add_input(input_id)
            
            elif line.startwith("OUTPUT"):
                output_id = line[line.find("(")+1:line.find(")")]
                circuit.add_output(output_id)
            
            elif "=" in line:
                gate_id,expr = line.split("=")
                gate_type,inputs_str = expr.split("(")
                inputs = inputs_str.rstrip(")").split(", ")
                gate - Gate(gate_id,gate_type)
                for input_id in inputs:
                    gate.add_fanin(input_id)
                circuit.add_gate(gate)
    return circuit

#  Liberty file parser

import numpy as np
class LibertyParser:
    def __init__(self,filename):
        # map the gate_type to the LUT in the lib for delay and slew
        self.delay_LUT = {}
        self.slew_LUT ={}
        # list of input slews
        self.input_slews=[]
        self.load_caps = []
        self.load_liberty_file(filename)

    def load_liberty_file(self,filename):
        # collects delay_LUTs, slew_LUT from liberty file
        pass
    def interpolate(self,lut,input_slew,load_cap):
        x = np.searchsorted(self.input_slews, input_slew)-1
        y = np.searchsorted(self.load_caps,load_cap)-1

        #  Boundary check and interpolation
        x1, x2 = self.input_slew[x],self.input_slews[x+1]
        y1, y2 = self.load_caps[y],slef.load_caps[y+1]
        f11,f12 = lut[x,y],lut[x,y+1]
        f21,f22 = lut[x+1,y],lut[x+1,y+1]

        # Bilinear interpolation formula

        f11 *
