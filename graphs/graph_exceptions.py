class NodeNotFoundError(Exception):
    """ raised when a node doesn't exist. """
    pass

class DuplicateKeyError(Exception):
    """ raised when a key already exists. """
    pass
