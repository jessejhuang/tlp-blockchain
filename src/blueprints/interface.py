'''
Routes interfaced by frontend
'''
import json
from flask import Blueprint, jsonify, request
from peers import request_peers
from src.blockchain.block import Block
from .. import database as db
from ..environment import ORIGIN_IP, PORT

interface = Blueprint('__interface__', __name__)

@interface.route('/print', methods=['GET'])
def get_node_info():
    '''
    allows us to see the chain, peers and last hash of the nodes blockchain
    '''
    node = db.get_node()
    request_peers("http://{}:{}".format(ORIGIN_IP, PORT))
    return jsonify(chain=node.chain,
                   peers=node.peers,
                   last_hash=node.last_hash
                  )

@interface.route('/add', methods=['POST'])
def receive_block():
    '''
    allows node to receive new blocks from user to share to network and begin validation
    '''
    node = db.get_node()
    new_block_data = request.get_json()
    new_block = Block(node.last_hash,
                      new_block_data['block']['check_number'],
                      new_block_data['block']['sender'],
                      new_block_data['block']['recipient'],
                      new_block_data['block']['amount']
                     )
    node.add_block(new_block, db.get_own_address())
    node.share_block(new_block, new_block_data, db.get_own_address())
    return jsonify(success=True)

@interface.route('/halt', methods=['POST'])
def update_chain():
    '''
    allows node to receive validated block from other nodes
    '''
    node = db.get_node()
    new_block_data = request.get_json()
    new_block = Block(node.last_hash,
                      new_block_data['check_number'],
                      new_block_data['sender'],
                      new_block_data['recipient'],
                      new_block_data['amount']
                     )
    node.chain.append(json.dumps(new_block.__dict__))
    data = '''New Block added to chain: Sender: {}\nRecipient: {}\nAmount: {}'''\
        .format(
            str(new_block_data['sender']),
            str(new_block_data['recipient']),
            new_block_data['amount']
        )
    return data
