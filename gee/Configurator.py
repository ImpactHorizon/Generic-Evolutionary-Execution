class Configurator(object):
    def __init__(self, source):
        self.source = source
        self.parameters = {}
        self.is_ready = False
        
    def read_configuration(self):
        raise RuntimeError("Configurator does not implement read_configuration,"
                            " please use concrete configurator type.")
        
    def __getitem__(self, key):
        if self.is_ready:
            return self.parameters[key]
        else:
            raise RuntimeError("Cannot obtain value from configurator before "
                                "reading configuration.")            