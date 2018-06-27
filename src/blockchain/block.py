import hashlib
import time

class Block:
    def __init__(self, data = 'Origin Block', prev_hash=None, timestamp=None):
        self.prev_hash = str(prev_hash) 
        self.data      = str(data)      
        if timestamp is None:
            self.timestamp = str(time.time())
        else:
            self.timestamp = str(timestamp)
        self.hash = compute_hash(self)

def compute_hash(block):
    return hashlib.sha512(
        bytes(block.data,      'utf-8') + 
        bytes(block.prev_hash, 'utf-8') + 
        bytes(block.timestamp, 'utf-8') 
        ).hexdigest()