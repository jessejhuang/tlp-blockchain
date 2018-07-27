'''
Block object and hash method used by Node
'''
import hashlib
import time, datetime
from hashlib import sha256


class Block:
    '''
    Attributes:
        prev_hash (str): Hash of the previous block
        checkNumber(int): Check number
        sender(str): person sending the check
        recipient(str): person receiving the check
        amount(int): amount transferred through the check
        timestamp (str): Time the block was generated
    '''
    def __init__(self, prev_hash = None, check_number = None, sender = None, recipient = None, amount = None, timestamp = None):
        if prev_hash is None:
            self.prev_hash = "00000000"
            self.sender = "Origin"
        else:
            self.prev_hash = str(prev_hash)
        self.check_number = check_number
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        if timestamp is None:
            self.timestamp = str(time.time())
        else:
            self.timestamp = str(timestamp)
        self.hash = compute_hash(self)

    def __repr__(self):
        '''
        String representation of a block
        '''
        return '''Check Number:\t%s\nTimestamp:\t%s\nPrev Hash:\t%s\nSender:\t%s\nRecipient:\t%s\nAmount:\t%s\n'''\
               %(self.check_number, datetime.datetime.fromtimestamp(int(float(self.timestamp))), self.prev_hash,self.sender, self.recipient,self.amount)

    def __eq__(self, other):
        '''
        Equality operator

        Invoked when 'blockA == blockB' is called
        '''
        return other and self.prev_hash == other.prev_hash \
            and self.check_number == other.check_number and self.timestamp == other.timestamp

def compute_hash(block):
    '''
    sha512 hash of block
    '''
    sha = sha256()
    sha.update((str(block.sender) + str(block.recipient) + str(block.amount) + str(block.timestamp)
                + str(block.prev_hash) + str(block.check_number)).encode())
    return sha.hexdigest()
