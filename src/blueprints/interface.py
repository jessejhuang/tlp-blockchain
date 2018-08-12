'''
Routes interfaced by frontend
'''
import json
from flask import Blueprint, jsonify, request
from src.blockchain.block import Block
from .. import database as db

interface = Blueprint('__interface__', __name__)

@interface.route('/print', methods=['GET'])
def get_node_info():
    '''
    allows us to see the chain, peers and last hash of the nodes blockchain
    '''
    node = db.get_node()
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
    return jsonify(success=True)

@interface.route('/recieve_chain', methods=['POST'])
def receive_chain():
    '''
    Another node sends its ledger; decide whether to adopt the change
    '''
    # node = db.get_node()
    new_chain_data = request.get_json()
    # new_block = Block(node.last_hash,
    #                   new_block_data['check_number'],
    #                   new_block_data['sender'],
    #                   new_block_data['recipient'],
    #                   new_block_data['amount']
    #                  )
    print(new_chain_data)
    print('new chain type: ', type(new_chain_data))
    return new_chain_data
