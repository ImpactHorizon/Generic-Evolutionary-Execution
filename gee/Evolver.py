import sys
from functools import partial
from pyevolve.Util import Graph
from pyevolve import GSimpleGA
from pyevolve import Consts
from pyevolve import Migration
from Util import (chain_validation, validate_type, validate_on_list, 
                    validate_in_range, validate_percent, validate_tcp_port, 
                    validate_host_reachable, validate_function_callable)

EVALUATION_PARAMS = { "migration" : [partial(validate_type, 
                                                expected_type=bool)], 
                        "islands" : [partial(validate_type, 
                                                expected_type=Graph)], 
                        "host" : [partial(validate_type, expected_type=str),
                                    validate_host_reachable], 
                        "port" : [partial(validate_type, expected_type=int),
                                    validate_tcp_port], 
                        "fitness_function" : [partial(validate_type, 
                                                        expected_type=str),
                                                validate_function_callable],
                        "optimization_type" : [partial(validate_type, 
                                                        expected_type=str),
                                                partial(validate_on_list, 
                                        acceptables=["minimize", "maximize"])], 
                        "population_size" : [partial(validate_type, 
                                                        expected_type=int),
                                                partial(validate_in_range, 
                                                acceptable=xrange(2, 1001))], 
                        "generations" : [partial(validate_type, 
                                                    expected_type=int),
                                            partial(validate_in_range, 
                                            acceptable=xrange(1, sys.maxint))], 
                        "mutation_rate" : [partial(validate_type, 
                                                    expected_type=float),
                                            validate_percent]}

class Evolver(object):
    __params__ = EVALUATION_PARAMS.keys()
    
    __validators__ = EVALUATION_PARAMS        
                    
    def __init__(self, configurator):         
        self.genome = None
        self.engine = None
        self.configurator = configurator
        
        self.slotsInitialization(Evolver)
    
    def slotsInitialization(self, cls):  
        print type(self)
        validators = getattr(cls, '__validators__', {})
        for slot_name in getattr(cls, '__params__', []):
            print slot_name
            value = self.configurator[slot_name]
            if validators[slot_name]:
                value = self.validate(slot_name, value, validators)
            setattr(self, slot_name, value)
                       
    def validate(self, name, value, validators):
        return chain_validation(value, validators[name], name)

    def createGenome(self):
        raise RuntimeError("Evolver is a base class without specified genome "
                            "type. Try using specialized Evolver.")
                            
    def createEngine(self):
        if self.genome:
            try:
                self.engine = GSimpleGA.GSimpleGA(self.genome)
            except:
                raise TypeError("Creating GA engine with specified genome "
                                "failed.")
        else:
            raise TypeError("Tried to create engine with empty genome.")
        
    def setUpEngine(self):
        self.engine.setPopulationSize(self.population_size)
        self.engine.setGenerations(self.generations)
        self.engine.setMinimax(Consts.minimaxType[self.optimization_type])
        self.engine.setMutationRate(self.mutation_rate)
        if self.migration:
            mig_adapter = Migration.WANMigration(self.host, self.port, "nd")
            mig_adapter.setTopology(self.islands)
            self.engine.setMigrationAdapter(mig_adapter)
        
    def run(self):
        self.createGenome()
        self.createEngine()
        self.setUpEngine()