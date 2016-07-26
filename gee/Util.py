import socket
import FitnessFunctions

def chain_validation(value, validators, name):    
    for validator in validators:        
        value=validator(value, name=name)
    return value

def validate_type(value, expected_type, name):
    if not type(value) is expected_type:
        try:
            value = expected_type(value)
        except:
            raise ValueError("Cannot convert %s value to %s" 
                                % (name, expected_type))        
    return value    

def validate_on_list(value, acceptables, name):
    assert(isinstance(acceptables, list))
    if not value in acceptables:
        raise ValueError("Value of %s is not on accepted values list - %s." 
                            % (name, acceptables))
    return value
    
def validate_in_range(value, acceptable, name):
    assert(isinstance(acceptable, xrange))
    if not value in acceptable:
        raise ValueError("Value of %s is not in range - %s." % (name, 
                                                                acceptable))
    return value

def validate_percent(value, name):
    if not ((value >= 0.0) and (value <= 1.0)):
        raise ValueError("Value of %s is not in percentage range - [0.0, 1.0]." 
                            % (name))
    return value

def validate_tcp_port(port, name):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('127.0.0.1', port))
    except:       
        raise ValueError("Value of %s is not accessible port (%s)." % (name, 
                                                                        port))
    return port
    
def validate_host_reachable(host, name):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((host, 0))
    except:       
        raise ValueError("Value of %s is not correct host (%s)." % (name, host))
    return host
    
def validate_function_callable(func_name, name):
    try:
        func = getattr(FitnessFunctions, func_name)
    except:
        raise ValueError("Value of %s (%s) is not function name from fitness "
                            "functions module" % (name, func_name))
    if not hasattr(func, '__call__'):
        raise ValueError("Value of %s (%s) is not callable function from "
                            "fitness functions module" % (name, func_name))
    return func_name