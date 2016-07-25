import unittest
from mock import MagicMock, patch
import sys
import random
import socket
from gee import Util

class ValidatorsTestCase(unittest.TestCase):    
    class Derived(object):
        pass
        
    @classmethod
    def setUpClass(cls):        
    
        ValidatorsTestCase.str_type = "str"
        ValidatorsTestCase.int_type = 10
        ValidatorsTestCase.float_type = 1.0
        ValidatorsTestCase.bool_type = True
        ValidatorsTestCase.object_type = object()
        ValidatorsTestCase.derived_type = ValidatorsTestCase.Derived()
        ValidatorsTestCase.acceptables = [1, 2, 4, "foo", 2.5]
        ValidatorsTestCase.max_range = 21
        ValidatorsTestCase.min_range = -2
        ValidatorsTestCase.expected_range = xrange(ValidatorsTestCase.min_range, 
                                                ValidatorsTestCase.max_range)   

    def test_type_correct(self):        
        self.assertEqual(ValidatorsTestCase.str_type, 
                            Util.validate_type(ValidatorsTestCase.str_type, 
                                                str, "test_str"))
        self.assertEqual(ValidatorsTestCase.int_type, 
                            Util.validate_type(ValidatorsTestCase.int_type, 
                                                int, "test_int"))
        self.assertEqual(ValidatorsTestCase.float_type, 
                            Util.validate_type(ValidatorsTestCase.float_type, 
                                                float, "test_float"))
        self.assertEqual(ValidatorsTestCase.bool_type, 
                            Util.validate_type(ValidatorsTestCase.bool_type, 
                                                bool, "test_bool"))
        self.assertEqual(ValidatorsTestCase.object_type, 
                            Util.validate_type(ValidatorsTestCase.object_type, 
                                                object, "test_object"))
        self.assertEqual(ValidatorsTestCase.derived_type, 
                            Util.validate_type(ValidatorsTestCase.derived_type, 
                                                ValidatorsTestCase.Derived, 
                                                "test_derived"))

        
    def test_type_incorrect(self):
        with self.assertRaises(ValueError): 
            Util.validate_type(ValidatorsTestCase.str_type, int, "test_str")
            
        with self.assertRaises(ValueError): 
            Util.validate_type(ValidatorsTestCase.int_type, float, "test_int")
            
        with self.assertRaises(ValueError): 
            Util.validate_type(ValidatorsTestCase.float_type, bool, 
                                "test_float")
            
        with self.assertRaises(ValueError): 
            Util.validate_type(ValidatorsTestCase.bool_type, object, 
                                "test_bool")
            
        with self.assertRaises(ValueError): 
            Util.validate_type(ValidatorsTestCase.object_type, 
                                ValidatorsTestCase.Derived, "test_object")
            
        with self.assertRaises(ValueError): 
            Util.validate_type(ValidatorsTestCase.derived_type, object, 
                                "test_derived")
                                
    def test_on_list_exists(self):
        self.assertEqual(ValidatorsTestCase.acceptables[-1], 
                            Util.validate_on_list(
                                ValidatorsTestCase.acceptables[-1], 
                                ValidatorsTestCase.acceptables, 
                                "test_list_float"))
        
        self.assertEqual(ValidatorsTestCase.acceptables[1], 
                            Util.validate_on_list(
                                ValidatorsTestCase.acceptables[1], 
                                ValidatorsTestCase.acceptables, 
                                "test_list_int"))
        
        self.assertEqual(ValidatorsTestCase.acceptables[3], 
                            Util.validate_on_list(
                                ValidatorsTestCase.acceptables[3], 
                                ValidatorsTestCase.acceptables, 
                                "test_list_str"))
    
    def test_on_list_not_exists(self):
        with self.assertRaises(ValueError): 
            Util.validate_on_list(None, ValidatorsTestCase.acceptables, 
                                    "test_list_non")
        
    def test_on_list_bad_acceptables(self):
        with self.assertRaises(AssertionError): 
            Util.validate_on_list(None, 5, "test_list_bad")
            
    def test_in_range_correct(self):
        value = random.randint(ValidatorsTestCase.min_range, 
                                ValidatorsTestCase.max_range-1)
        self.assertEqual(value, Util.validate_in_range(value, 
                                    ValidatorsTestCase.expected_range, 
                                    "test_range_in"))
                                    
    def test_in_range_incorrect(self):
        with self.assertRaises(ValueError):
            Util.validate_in_range(-4, ValidatorsTestCase.expected_range, 
                                    "test_range_out")
                                    
    def test_in_range_bad_acceptables(self):
        with self.assertRaises(AssertionError):
            Util.validate_in_range(0, [0, 1, 2], "test_range_bad")
            
    def test_percent_correct(self):
        value = 0.2
        self.assertEqual(0.2, Util.validate_percent(value, "test_percent_ok"))
        
    def test_percent_incorrect(self):
        values = [1.3, -0.2, 100]
        for val in values:
            print val
            with self.assertRaises(ValueError):
                Util.validate_percent(val, "test_percent_bad")
                
    def test_port_correct(self):
        port = "8080"
        self.assertEqual(port, Util.validate_tcp_port(port, "test_port_ok"))
                                                    
    def test_port_incorrect(self):
        port = "8080"
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.bind(('127.0.0.1', int(port)))        
        with self.assertRaises(ValueError):
            Util.validate_tcp_port(port, "test_port_bad")
            
    def test_host_reachable(self):
        host = "127.0.0.1"
        self.assertEqual(host, Util.validate_host_reachable(host, 
                                                            "test_host_ok"))
        
    def test_host_unreachable(self):
        host = "chicken-party"
        with self.assertRaises(ValueError):
            self.assertEqual(host, Util.validate_host_reachable(host, 
                                                            "test_host_bad"))
    def test_function_exists(self):
        sys.modules['gee.FitnessFunctions'].shakaron_makaron = MagicMock()
        func_name = 'shakaron_makaron'
        self.assertEqual(func_name, Util.validate_function_callable(
                                            func_name, "test_func_ok"))
        sys.modules['gee.FitnessFunctions'].shakaron_makaron = None
        
    def test_function_not_exists(self):
        func_name = 'shakaron_makaron'
        with self.assertRaises(ValueError):
            Util.validate_function_callable(func_name, "test_func_bad")