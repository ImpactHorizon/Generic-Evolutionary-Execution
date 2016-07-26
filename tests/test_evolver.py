import unittest
from mock import MagicMock
import sys
from pyevolve.Util import Graph
from pyevolve import GenomeBase
from pyevolve import Consts
from gee import Evolver

class EvolverConstructionTestCase(unittest.TestCase):
    def setUp(self):
        self.params = {"migration" : True, 
                        "islands" : Graph(), 
                        "host" : "localhost", 
                        "port" : "1020", 
                        "fitness_function" : "BestFit",
                        "optimization_type" : "minimize", 
                        "population_size" : "100", 
                        "generations" : "10000000", 
                        "mutation_rate" : "0.7832"}
    
        def get_item(arg):
            return self.params[arg]
            
        self.configurator = MagicMock()
        self.configurator.__getitem__ = MagicMock(side_effect=get_item)

    def test_contruction_ok(self):
        sys.modules['gee.FitnessFunctions'].BestFit = MagicMock()
        evolver=Evolver.Evolver(self.configurator)
        self.assertTrue(evolver is not None) 
        sys.modules['gee.FitnessFunctions'].BestFit = None
        
    def test_construction_bad_islands(self):
        self.params["islands"] = None
        with self.assertRaises(ValueError):
            evolver=Evolver.Evolver(self.configurator)
        
    def test_construction_bad_host(self):
        self.params["host"] = 123
        with self.assertRaises(ValueError):
            evolver=Evolver.Evolver(self.configurator)
        
    def test_construction_bad_port(self):
        self.params["port"] = "port"
        with self.assertRaises(ValueError):
            evolver=Evolver.Evolver(self.configurator)
        
    def test_construction_bad_fitness_function(self):
        self.params["fitness_function"] = "bad_func"
        with self.assertRaises(ValueError):
            evolver=Evolver.Evolver(self.configurator)
        
    def test_construction_bad_optimization_type(self):
        self.params["optimization_type"] = "RandomType"
        with self.assertRaises(ValueError):
            evolver=Evolver.Evolver(self.configurator)
        
    def test_construction_bad_population_size(self):
        self.params["population_size"] = 1000000000
        with self.assertRaises(ValueError):
            evolver=Evolver.Evolver(self.configurator)
        
    def test_construction_bad_generations(self):
        self.params["generations"] = -4
        with self.assertRaises(ValueError):
            evolver=Evolver.Evolver(self.configurator)
        
    def test_construction_bad_mutation_rate(self):
        self.params["mutation_rate"] = "1010"
        with self.assertRaises(ValueError):
            evolver=Evolver.Evolver(self.configurator)
            
class EvolverMethodsTestCase(unittest.TestCase):
    def setUp(self):
        self.params = {"migration" : True, 
                        "islands" : Graph(), 
                        "host" : "localhost", 
                        "port" : "1020", 
                        "fitness_function" : "BestFit",
                        "optimization_type" : "minimize", 
                        "population_size" : "100", 
                        "generations" : "10000000", 
                        "mutation_rate" : "0.7832"}
    
        def get_item(arg):
            return self.params[arg]
            
        self.configurator = MagicMock()
        self.configurator.__getitem__ = MagicMock(side_effect=get_item)
        
        sys.modules['gee.FitnessFunctions'].BestFit = MagicMock()        
        self.evolver = Evolver.Evolver(self.configurator)
        sys.modules['gee.FitnessFunctions'].BestFit = None
        
    def test_create_genome(self):
        with self.assertRaises(RuntimeError):
            self.evolver.createGenome()
        self.assertEqual(None, self.evolver.genome)
            
    def test_create_engine_from_empty_genome(self):
        with self.assertRaises(TypeError):
            self.evolver.createEngine()
            
    def test_create_engine_from_bad_genome(self):
        self.evolver.genome = object()
        with self.assertRaises(TypeError):
            self.evolver.createEngine()
            
    def test_setup_engine(self):
        self.evolver.genome = GenomeBase.GenomeBase()
        self.evolver.createEngine()
        self.evolver.setUpEngine()
        engine = self.evolver.engine
        
        self.assertEqual(engine.getGenerations(), int(self.evolver.generations))
        self.assertEqual(engine.getMinimax(), 
                            Consts.minimaxType[self.evolver.optimization_type])
        self.assertEqual(engine.pMutation, self.evolver.mutation_rate)
        self.assertEqual(engine.internalPop.popSize, 
                            self.evolver.population_size)
                            
        self.assertTrue(engine.migrationAdapter is not None)
                            
        