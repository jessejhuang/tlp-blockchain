import copy
import random

from blockchain.block import Block, compute_hash

class Node:
    def __init__(self, index, original=None):
        """ Create node from scratch or from another node"""
        self.index = index
        self.chain = []
        if original is None:
            self.chain.append(Block())
            self.last_hash = self.chain[-1].hash
        else:
            self.chain = self.copy_chain(original)
            self.last_hash = original.last_hash
    
    def copy_chain(self, node):
        chain = []
        for block in node.chain:
            chain.append(Block(block.data, block.prev_hash, block.timestamp))
        return chain
        
    def is_valid(self, node):
        """ Check if a node's chain is valid by by checking against hashes of own chain"""
        if len(node.chain) < len(self.chain):
            return False
        prev_hash = 'None'
        for i, block in enumerate(self.chain):
            other_block = node.chain[i]
            if prev_hash != other_block.prev_hash or block.hash != compute_hash(other_block):
                return False
            prev_hash = block.hash
        return True
    
    def do_work(self):
        """ Models time it takes a node to solve a block as a random number"""
        return random.randint(0, 1000)

    def update_chain(self, network):
        """ Set chain to be that of the node with the longest valid chain """
        self.chain = max(network, key=lambda node: len(node.chain) * self.is_valid(node)).chain
        self.last_hash = self.chain[-1].hash

    def add_block(self, block, network):
        """ Add new block and inform network """
        self.chain.append(block)
        self.last_hash = block.hash
        self.update_chain(network)
