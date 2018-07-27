'''
Node object that manages blockchain data and communicates with peers
'''
import requests

from block import Block, compute_hash
#from pyp2py.net import *
import json

class Node:
    '''
    Attributes
        chain (list(str)): The blockchain; represented as list of blocks
        peers (list(str)): List of URLs of connected nodes
        last_hash (str): Hash of the last block in the chai
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
            #s = json.dumps(foo.__dict__)
            origin = Block()
            self.last_hash = origin.hash
            self.chain.append(json.dumps(Block().__dict__))
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
        '''self.proofOfWork(block)
        Add new block and inform network
        '''
        self.proofOfWork(block)
        self.chain.append(json.dumps(block.__dict__))
        self.last_hash = block.hash
        #temporarily commented out while developing
        #self.update_chain(network)



    def proofOfWork(self, block):
        '''
        Used as our method of consensus, requires any given node to perform a heavily computational
        task before being able to add a block to the blockchain. ensures that no single
        node can surpass the compulational power of the rest of the nodes combined on the network
        #difficulty is hardcoded as 5,
        :param block:
        :return:
        '''
        block.nonce = 0
        hash = block.hash
        #will update a block's nonce attribute until the hash of the block starts with a determined number of zeroes
        #updating the nonce will cause the block to have a new hash.
        while not block.hash.startswith("0"* 5):
            block.nonce += 1
            block.hash = compute_hash(block)
        #print(block.nonce)
        #print(block.hash)

n = Node()
#print(n.last_hash)
b = Block()
n.add_block(b,n.peers)
#print(n.last_hash)