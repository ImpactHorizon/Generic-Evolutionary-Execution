from functools import partial
from pyevolve import G2DCartesian
from Evolver import Evolver
from Util import validate_type, validate_in_range

EVALUATION_PARAMS = { "rows" : [partial(validate_type, expected_type=int), 
                                partial(validate_in_range, 
                                        acceptable=xrange(1, 1000))], 
                        "cols" : [partial(validate_type, expected_type=int), 
                                    partial(validate_in_range, 
                                        acceptable=xrange(1, 1000))], 
                        "inputs" : [partial(validate_type, expected_type=int), 
                                    partial(validate_in_range, 
                                            acceptable=xrange(1, 1000))], 
                        "outputs" : [partial(validate_type, expected_type=int), 
                                        partial(validate_in_range, 
                                                acceptable=xrange(1, 1000))]}

class CGPEvolver(Evolver):
    __params__ = EVALUATION_PARAMS.keys()
    
    __validators__ = EVALUATION_PARAMS

    def __init__(self, configurator):
        super(CGPEvolver, self).__init__(configurator)
        self.slotsInitialization(CGPEvolver)
        
    def createGenome(self):
        self.genome = G2DCartesian.G2DCartesian(self.rows, self.cols, 
                                                self.inputs, self.outputs)        