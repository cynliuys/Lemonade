# finished
import redis
import hashlib

def encode(str, code='utf-8'):
    return str.encode(code) 

def decode(bytes, code='utf-8'):
    return bytes.decode(code)
    
def sum256(*args):
    m = hashlib.sha256()
    for arg in args:
        m.update(arg) 
    return m.hexdigest()
    # https://docs.python.org/3/library/hashlib.html

class ContinueIt(Exception):
    pass

class BreakIt(Exception):
    pass
