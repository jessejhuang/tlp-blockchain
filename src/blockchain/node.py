'''
Node object that manages blockchain data and communicates with peers
'''
import random
import json
import requests
from block import Block, compute_hash

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
        '''
        Attempt to add block by starting proof of work
        '''
        self.proof_of_work(block, url)

    def share_block(self, block, block_data, current_url):
        '''
        Once a block has been added to the chain, inform other peers to stop doing work
        :param block: new block being shared throughout the network
        :param seen_nodes: keeps track of what nodes have already received the block
        :param current_url: the node's current url passed in from the server instance
        :return:
        '''
        seen_nodes = block_data['seen_nodes']
        block_data['seen_nodes'].append(current_url)
        seen_nodes.append(current_url)
        current_instance = current_url.split("//")[1] # get ngrok url regardless of http or https
        other_nodes = [peer for peer in self.peers if current_instance not in peer]
        for __ in range(5): # Randomly select 5 peers to share block to
            random_node = random.choice(other_nodes)
            if random_node not in seen_nodes:
                try:
                    if requests.get(random_node).status_code == 200:
                        block_data['hash'] = block.hash
                        block_data['block']['timestamp'] = block.timestamp
                        requests.post(random_node + "/halt", json=block.__dict__)
                        seen_nodes.append(random_node)
                except (ConnectionRefusedError,
                        requests.exceptions.ConnectionError,
                        requests.exceptions.MissingSchema):
                    block_data['seen_nodes'].append(random_node)
                    seen_nodes.append(random_node)

    def proof_of_work(self, block, url):
        '''
        Used as our method of consensus, requires any given node to perform a heavily computational
        task before being able to add a block to the blockchain. ensures that no single
        node can surpass the compulational power of the rest of the nodes combined on the network
        #difficulty is hardcoded as 5,

        only attempts to validate while node chain length is unchanged,
        a change in node chain length implies that another node has completed
        validation of the block
        :param block:
        :return:
        '''
        original_chain_length = len(self.chain)
        block.nonce = 0
        while len(self.chain) == original_chain_length:
            valid_hash = block.hash
            if valid_hash.startswith('0'*5):
                self.chain.append(json.dumps(block.__dict__))
                self.last_hash = block.hash
                self.halt_network_validation(block, url)
                return
            block.nonce += 1
            block.hash = compute_hash(block)
        #will update a block's nonce attribute until the hash of the block
        # starts with a determined number of zeroes
        #updating the nonce will cause the block to have a new hash.

    def halt_network_validation(self, block, url):
        '''
        Call /halt route of all routes
        '''
        data = {"halted_nodes": []}
        data['halted_nodes'].append(url)
        for peer in self.peers:
            if peer not in data['halted_nodes'] and url != peer:
                try:
                    requests.post('{}/halt'.format(peer), json={json.dumps(block.__dict__)})
                except (TypeError,
                        ConnectionRefusedError,
                        requests.exceptions.MissingSchema,
                        requests.exceptions.ConnectionError):
                    continue
