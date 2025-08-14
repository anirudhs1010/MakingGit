import os
import hashlib

GIT_DIR = '.anigit'


def init ():
    os.makedirs(GIT_DIR)
    os.makedirs(f'{GIT_DIR}/objects')

def hash_object (data, type_ = 'blob'): #allows us to store objectes and opens this in the given directory
    obj = type_.encode () + b'\x00' + data
    oid = hashlib.sha1(obj).hexdigest() #currently using sha-1 hash but apparently the current Git implementation use SHA-256 due to hash collisions in SHA-1
    with open(f'{GIT_DIR}/objects/{oid}', 'wb') as out: #writes it to our "object" database
        out.write(obj)
    return oid

def get_object(oid, expected ='blob'):
    with open(f'{GIT_DIR}/objects/{oid}', 'rb') as f:
        obj = f.read()
    type_, _, content = obj.partition(b'\x00') #
    type_ = type_.decode()
    if expected is not None:
        assert type_ == expected, f'Expected {expected}, got {type_}'
    return content