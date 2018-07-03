'''
node.py test file
'''
from blockchain.block import Block
from blockchain.node import Node

def test_chain_is_valid():
    '''
    Basic test of node.is_valid() method
    '''
    node_a = Node()
    node_b = Node(original=node_a)
    valid_block = Block("Foo", node_b.last_hash)
    node_c = Node() #Created with different origin block than a or b, so should always be invalid
    network = []
    network.append(node_a)
    network.append(node_b)
    network.append(node_c)
    node_a.add_block(valid_block, network)
    assert node_b.is_valid(node_a)
    assert not node_a.is_valid(node_b) # b does not yet contain the block added to a
    node_b.update_chain(network)   # b adopts a's
    assert node_a.is_valid(node_b)
    assert not node_c.is_valid(node_a)
    assert not node_c.is_valid(node_b)
    assert not node_a.is_valid(node_c)
    assert not node_b.is_valid(node_c)
