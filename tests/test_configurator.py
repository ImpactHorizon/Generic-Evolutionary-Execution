import unittest
from gee import Configurator

class ConfiguratorTestCase(unittest.TestCase):
    def setUp(self):
        self.source = object()

    def test_configurator_construction(self):             
        conf = Configurator.Configurator(self.source)
        self.assertEqual(self.source, conf.source)
        self.assertFalse(conf.parameters)
        self.assertFalse(conf.is_ready)
        
    def test_configurator_read(self):
        conf = Configurator.Configurator(self.source)
        with self.assertRaises(RuntimeError):
            conf.read_configuration()
            
    def test_configurator_get_item_not_ready(self):
        conf = Configurator.Configurator(self.source)
        with self.assertRaises(RuntimeError):
            conf['aaa']
            
    def test_configurator_get_item_no_key(self):
        conf = Configurator.Configurator(self.source)
        conf.is_ready = True
        with self.assertRaises(KeyError):
            conf['aaa']
    
    def test_configurator_get_item_ok(self):
        conf = Configurator.Configurator(self.source)
        conf.parameters['aaa'] = 10
        conf.is_ready = True
        self.assertEqual(conf['aaa'], 10)