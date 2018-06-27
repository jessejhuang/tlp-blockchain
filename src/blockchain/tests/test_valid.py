from blockchain.block import Block
from blockchain.node import Node 

def test_chain_is_valid():
    a = Node(0)
    b = Node(1, original=a)
    valid_block = Block("Foo", b.last_hash)
    c = Node(2) #Created with different origin block than a or b, so should always be invalid 
    network = []
    network.append(a)
    network.append(b)
    network.append(c)
    a.add_block(valid_block, network)
    assert(b.is_valid(a))
    assert(not a.is_valid(b)) # b does not yet contain the block added to a
    b.update_chain(network)   # b adopts a's
    assert(a.is_valid(b))
    assert(not c.is_valid(a))
    assert(not c.is_valid(b))
    assert(not a.is_valid(c))
    assert(not b.is_valid(c))
    
    
