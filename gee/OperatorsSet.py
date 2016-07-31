import types

class OperatorsSet(object):
    def __init__(self, name):                                                         
        self.operators = []
        self.name = name
        self.params = []
        self.keeper = None
        self.initializeModule(name)
        self.register("gee.operators.%s" % (self.name), dir(self.keeper)) 

    def initializeModule(self, name):
        exec("from operators import %s as keeper" % (name))
        if not hasattr(keeper.operand_types, "__iter__"):
            raise ValueError("Operand types must be a list.")
            
        self.keeper = keeper 
        self.operand_types = keeper.operand_types
        
    def register(self, module, functions):
        self.operators = []
        self.module_name = module
        for func in functions:
            try:
                exec("from %s import %s" % (module, func))
            except:
                raise ImportError("Cannot import function %s from operators %s" 
                                    % (func, module))
            exec("func_obj = %s" % (func))  
            
            if isinstance(func_obj, types.FunctionType):
                self.operators.append("%s.%s" % (module, func));        
        
    def inject(self, prefix):
        import __main__ as mod_main
        for operator in self.operators:
            op_name = operator.split('.')[-1]
            mod_name = '.'.join(operator.split('.')[:-1])
            gp_name = prefix + op_name
            exec("from %s import %s as %s" % (mod_name, op_name, gp_name))
            exec("func_obj = %s" % (gp_name))
            setattr(mod_main, gp_name, func_obj)