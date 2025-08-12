import os


GIT_DIR = '.anigit'


def init ():
    os.makedirs(GIT_DIR)
    os.makedirs(f'{GIT_DR}/objects')

def hash_object (data): #allows us to store objectes and opens this in the given directory
    oid = hashlib.sha1(data).hexdigest() #currently using sha-1 hash 
    with open(f'{GIT_DIR}/objects/{oid}', 'wb') as out: #writes it to our "object" database
        out.write (data)
    return oid