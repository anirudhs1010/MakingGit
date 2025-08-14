import os

from . import data


def write_tree (directory='.'):
    entries = []
    with os.scandir (directory) as it:
        for entry in it:
            full = f'{directory}/{entry.name}'
            if is_ignored (full): #in the git ignore file then just continue
                continue

            if entry.is_file (follow_symlinks=False):
                type_ = 'blob'
                with open (full, 'rb') as f:
                    oid = data.hash_object (f.read ())
            elif entry.is_dir (follow_symlinks=False):
                type_ = 'tree'
                oid = write_tree (full)
            entries.append ((entry.name, oid, type_)) #storing all of the updated files or directories listed

    tree = ''.join (f'{type_} {oid} {name}\n'
                    for name, oid, type_
                    in sorted (entries)) #entries are used here and joined to make a proper tree object that can be encoded
    return data.hash_object (tree.encode (), 'tree')

def _iter_tree_entries (oid): #helps go through all entries of a tree
    if not oid:
        return
    tree = data.get_object (oid, 'tree')
    for entry in tree.decode ().splitlines ():
        type_, oid, name = entry.split (' ', 2) #splits up the entry and decodes it so it can be parsed
        yield type_, oid, name


def get_tree (oid, base_path=''):
    result = {}
    for type_, oid, name in _iter_tree_entries (oid): #iter tree called here so it can be parsed
        assert '/' not in name
        assert name not in ('..', '.')
        path = base_path + name
        if type_ == 'blob':
            result[path] = oid #map of path and oid
        elif type_ == 'tree':
            result.update(get_tree (oid, f'{path}/')) #recursively tries to get the tree maybe we can optimize it to be a loop?
        else:
            assert False, f'Unknown tree entry {type_}'
    return result

def _empty_current_directory ():
    for root, dirnames, filenames in os.walk ('.', topdown=False):
        for filename in filenames:
            path = os.path.relpath (f'{root}/{filename}')
            if is_ignored (path) or not os.path.isfile (path):
                continue
            os.remove (path)
        for dirname in dirnames:
            path = os.path.relpath (f'{root}/{dirname}')
            if is_ignored (path):
                continue
            try:
                os.rmdir (path)
            except (FileNotFoundError, OSError):
                # Deletion might fail if the directory contains ignored files,
                # so it's OK
                pass
def read_tree (tree_oid):
    _empty_current_directory ()
    print(f"Reading tree with OID: {tree_oid}") 
    for path, oid in get_tree (tree_oid, base_path='./').items (): #
        os.makedirs (os.path.dirname (path), exist_ok=True)
        with open (path, 'wb') as f:
            
            f.write (data.get_object (oid))
            


def is_ignored (path):
    return '.anigit' in path.split ('/')