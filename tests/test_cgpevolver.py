import unittest
from mock import MagicMock, patch
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
                        "outputs" : 1,
                        "operators" : "FakeOperators"}
                            
        def get_item(arg):
            return self.params[arg]
            
        self.configurator = MagicMock()
        self.configurator.__getitem__ = MagicMock(side_effect=get_item)
        
        def fake_initialize(name):
            if name == "FakeOperators":                
                return
            else:
                raise ImportError("no operators")
                
        def fake_register(module, functions):
            return
        
        self.patcher_register = patch("gee.CGPEvolver.OperatorsSet.register")
        self.patcher_initialize = patch(
                                "gee.CGPEvolver.OperatorsSet.initializeModule")
        self.mock_initialize = self.patcher_initialize.start()
        self.mock_register = self.patcher_register.start()
        self.mock_initialize.side_effect = fake_initialize
        self.mock_register.side_effect = fake_register
                
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
            
    def test_construction_bad_operators(self):
        self.params['operators'] = 'BadOperators'
        with self.assertRaises(ValueError):
            CGPEvolver.CGPEvolver(self.configurator)
            
    def tearDown(self):
        self.patcher_initialize.stop()
        self.patcher_register.stop()
        
class CGPEvolverMethodsTestCase(unittest.TestCase):
    def setUp(self):
        self.params = {"migration" : False, 
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
                        "outputs" : 1,
                        "operators" : "FakeOperators"}
                            
        def get_item(arg):
            return self.params[arg]
            
        self.configurator = MagicMock()
        self.configurator.__getitem__ = MagicMock(side_effect=get_item)
        self.mock_module = MagicMock()  
        self.mock_module.operand_types = ['toys']
        
        sys.modules['gee.FitnessFunctions'].BestFit = MagicMock()
        sys.modules['gee.operators.FakeOperators'] = self.mock_module 

        def fake_initialize(name):
            if name == "FakeOperators":                
                return
            else:
                raise ImportError("no operators")
                
        def fake_register(module, functions):
            return
        
        self.patcher_register = patch("gee.CGPEvolver.OperatorsSet.register")
        self.patcher_initialize = patch(
                                "gee.CGPEvolver.OperatorsSet.initializeModule")
        self.mock_initialize = self.patcher_initialize.start()
        self.mock_register = self.patcher_register.start()
        self.mock_initialize.side_effect = fake_initialize
        self.mock_register.side_effect = fake_register
        
        self.evolver = CGPEvolver.CGPEvolver(self.configurator)
                
        sys.modules['gee.FitnessFunctions'].BestFit = None
        sys.modules['gee.operators.FakeOperators'] = None        
                
    def test_create_genome(self):
        self.evolver.createGenome()
        genome = self.evolver.genome
        self.assertEqual(genome.rows, self.evolver.rows)
        self.assertEqual(genome.cols, self.evolver.cols)
        self.assertEqual(genome.inputs, self.evolver.inputs)
        self.assertEqual(genome.outputs, self.evolver.outputs)     
        
    def test_setup_engine(self):
        def fake_inject(prefix):
            import __main__ as mod_main
            setattr(mod_main, "gp_fake", "fake_inject")

        self.evolver.operators = MagicMock()
        self.evolver.operators.inject = MagicMock(side_effect = fake_inject)    
        self.evolver.createGenome()
        self.evolver.createEngine()
        self.evolver.setUpEngine()
        engine = self.evolver.engine
        self.assertEqual(engine.elitism, True)
        self.assertEqual(engine.getParam("gp_function_prefix"), 
                            self.evolver.functions_prefix)
        import __main__ as mod_main
        self.assertTrue(hasattr(mod_main, "gp_fake"))
        
    def tearDown(self):
        self.patcher_initialize.stop()
        self.patcher_register.stop()
        