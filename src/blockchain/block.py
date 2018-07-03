'''
Block object and hash method used by Node
'''
import hashlib
import time

class Block:
    '''
    Attributes:
        prev_hash (str): Hash of the previous block
        data (str): Data stored in block (publicly available)
        timestamp (str): Time the block was generated
    '''
    def __init__(self, data='Origin Block', prev_hash=None, timestamp=None):
        self.prev_hash = str(prev_hash)
        self.data = str(data)
        if timestamp is None:
            self.timestamp = str(time.time())
        else:
            self.timestamp = str(timestamp)
        self.hash = compute_hash(self)

    def __repr__(self):
        '''
        String representation of a block
        '''
        return '''Block \n
                  ------\n
                  Data:\t%s\n
                  Timestamp:\t%s\n
                  Prev Hash:\t%s
               '''\
               %(self.data, self.timestamp, self.prev_hash)

    def __eq__(self, other):
        '''
        Equality operator

        Invoked when 'blockA == blockB' is called
        '''
        return other and self.prev_hash == other.prev_hash \
            and self.data == other.data and self.timestamp == other.timestamp

def compute_hash(block):
    '''
    sha512 hash of block
    '''
    return hashlib.sha512(
        bytes(block.data, 'utf-8') +
        bytes(block.prev_hash, 'utf-8') +
        bytes(block.timestamp, 'utf-8')
        ).hexdigest()
