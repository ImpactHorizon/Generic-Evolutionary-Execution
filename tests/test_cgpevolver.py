import unittest
from mock import MagicMock
import sys
from pyevolve.Util import Graph
from gee import CGPEvolver

class CGPEvolverConstructionTestCase(unittest.TestCase):
    def setUp(self):
        self.params = {"migration" : True, 
                        "islands" : Graph(), 
                        "host" : "localhost", 
                        "port" : "1020", 
                        "fitness_function" : "BestFit",
                        "optimization_type" : "minimize", 
                        "population_size" : "100", 
                        "generations" : "10000000", 
                        "mutation_rate" : "0.7832",
                        "rows" : 4,
                        "cols" : "6",
                        "inputs" : 2,
                        "outputs" : 1}
                            
        def get_item(arg):
            return self.params[arg]
            
        self.configurator = MagicMock()
        self.configurator.__getitem__ = MagicMock(side_effect=get_item)

    def test_construction_ok(self):
        sys.modules['gee.FitnessFunctions'].BestFit = MagicMock()
        evolver = CGPEvolver.CGPEvolver(self.configurator)
        sys.modules['gee.FitnessFunctions'].BestFit = None
        self.assertTrue(evolver is not None) 
        
    def test_construction_bad_rows(self):
        self.params["cols"] = 0
        with self.assertRaises(ValueError):
            CGPEvolver.CGPEvolver(self.configurator)
        
    def test_construction_bad_cols(self):
        self.params["rows"] = 0
        with self.assertRaises(ValueError):
            CGPEvolver.CGPEvolver(self.configurator)
        
    def test_construction_bad_inputs(self):
        self.params["inputs"] = "-5"
        with self.assertRaises(ValueError):
            CGPEvolver.CGPEvolver(self.configurator)
    
    def test_construction_bad_outputs(self):
        self.params["outputs"] = 2000
        with self.assertRaises(ValueError):
            CGPEvolver.CGPEvolver(self.configurator)
        
class CGPEvolverMethodsTestCase(unittest.TestCase):
    def setUp(self):
        self.params = {"migration" : True, 
                        "islands" : Graph(), 
                        "host" : "localhost", 
                        "port" : "1020", 
                        "fitness_function" : "BestFit",
                        "optimization_type" : "minimize", 
                        "population_size" : "100", 
                        "generations" : "10000000", 
                        "mutation_rate" : "0.7832",
                        "rows" : 4,
                        "cols" : "6",
                        "inputs" : 2,
                        "outputs" : 1}
                            
        def get_item(arg):
            return self.params[arg]
            
        self.configurator = MagicMock()
        self.configurator.__getitem__ = MagicMock(side_effect=get_item)
        
        sys.modules['gee.FitnessFunctions'].BestFit = MagicMock()        
        self.evolver = CGPEvolver.CGPEvolver(self.configurator)
        sys.modules['gee.FitnessFunctions'].BestFit = None

    def test_create_genome(self):
        self.evolver.createGenome()
        genome = self.evolver.genome
        self.assertEqual(genome.rows, self.evolver.rows)
        self.assertEqual(genome.cols, self.evolver.cols)
        self.assertEqual(genome.inputs, self.evolver.inputs)
        self.assertEqual(genome.outputs, self.evolver.outputs)