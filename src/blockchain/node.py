'''
Node object that manages blockchain data and communicates with peers
'''
import requests

from block import Block, compute_hash
#from pyp2py.net import *
import json
import requests

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

    def add_block(self, block, url):
        '''self.proofOfWork(block)
        Add new block after receiving it from user or network
        '''

        self.proofOfWork(block,url)
        #print("REAL VALIDATION ADD")
        self.chain.append(json.dumps(block.__dict__))
        self.last_hash = block.hash


    def share_block(self, block, block_data, current_url):
        '''

        :param block: new block being shared throughout the network
        :param seen_nodes: keeps track of what nodes have already received the block
        :param current_url: the node's current url passed in from the server instance
        :return:
        '''
        seen_nodes = block_data["seen_nodes"]
        block_data["seen_nodes"].append(current_url)
        seen_nodes.append(current_url)
        #self.peers = [peer for peer in self.peers if peer != current_url] #removes all instances of current url from shared peers
        current_instance = current_url.split("//")[1] #gets ngrok instance regardless of http or https
        for peer in self.peers:
            if peer not in seen_nodes and current_instance not in peer:
                try:
                    if requests.get(peer).status_code == 200:
                        #print(current_url)
                        #print(peer)
                        #block_data["seen_nodes"].append(current_url)
                        #requests.post(peer+"/add", json=block_data)
                        requests.post(peer + "/halt", json=block_data)
                        seen_nodes.append(peer)
                        #print(block_data["seen_nodes"])
                except:
                    block_data["seen_nodes"].append(peer)
                    seen_nodes.append(peer)


    def proofOfWork(self, block, url):
        '''
        Used as our method of consensus, requires any given node to perform a heavily computational
        task before being able to add a block to the blockchain. ensures that no single
        node can surpass the compulational power of the rest of the nodes combined on the network
        #difficulty is hardcoded as 5,

        only attempts to validate while node chain length is unchanged,
        a change in node chain length implies that another node has completed validation of the block
        :param block:
        :return:
        '''
        original_chain_length = len(self.chain)
        block.nonce = 0
        while len(self.chain) == original_chain_length:
            hash = block.hash
            if hash.startswith("0"*5):
                self.haltNetworkValidation(block, url)
                return
            block.nonce += 1
            block.hash = compute_hash(block)
        #will update a block's nonce attribute until the hash of the block starts with a determined number of zeroes
        #updating the nonce will cause the block to have a new hash.

    def haltNetworkValidation(self, block, url):
        data = {"halted_nodes": []}
        data['halted_nodes'].append(url)
        for peer in self.peers:
            if peer not in data['halted_nodes'] and url != peer:
                try:
                    requests.post(peer + "/halt", json={json.dumps(block.__dict__)})
                except:
                    continue