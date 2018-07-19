'''
Node object that manages blockchain data and communicates with peers
'''
from block import Block, compute_hash

class Node:
    '''
    Attributes
        chain (list(str)): The blockchain; represented as list of blocks
        peers (list(str)): List of URLs of connected nodes
        last_hash (str): Hash of the last block in the chain
    '''
    def __init__(self, original=None):
        '''
        Create node from scratch or from another node
        Args:
            original (Node): node to copy if __init__ invoked as copy constructor
        '''
        self.chain = []
        self.peers = []
        if original is None:
            self.chain.append(Block())
            self.last_hash = self.chain[-1].hash
        else:
            self.copy_chain(original)
            self.peers = original.peers
            self.last_hash = original.last_hash

    def copy_chain(self, node):
        '''
        Copy another node's chain
        '''
        self.chain = []
        for block in node.chain:
            self.chain.append(Block(block.data, block.prev_hash, block.timestamp))


    def is_valid(self, node):
        '''
        Check if a node's chain is valid by by checking against hashes of own chain
        '''
        if len(node.chain) < len(self.chain):
            return False
        prev_hash = 'None'
        for i, block in enumerate(self.chain):
            other_block = node.chain[i]
            if prev_hash != other_block.prev_hash or block.hash != compute_hash(other_block):
                return False
            prev_hash = block.hash
        return True

    def update_chain(self, network):
        '''
        Set chain to be that of the node with the longest valid chain
        '''
        self.chain = max(network, key=lambda node: len(node.chain) * self.is_valid(node)).chain
        self.last_hash = self.chain[-1].hash

    def add_block(self, block, network):
        '''
        Add new block and inform network
        '''
        self.chain.append(block)
        self.last_hash = block.hash
        self.update_chain(network)
