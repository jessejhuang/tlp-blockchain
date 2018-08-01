'''
Request or return connected nodes
'''
import requests
from flask import Blueprint, jsonify, request
from src import database as db

peers = Blueprint('__peers__', __name__)

@peers.route('/peers', methods=['POST'])
def send_peers():
    '''
    Input json:
        {
            url: requester_url string
        }
    Returns:
        list(str) of urls of currently connected nodes
    '''
    input_json = request.get_json(force=True)
    requester_url = input_json.get('url')
    connected_nodes = db.get_connected_nodes()
    if requester_url and requester_url not in connected_nodes:
        connected_nodes.append(requester_url)

    peer_list = None
    if connected_nodes[:-1]: # If len(connected_nodes not including requester) > 1
        peer_list = {'peers': tuple(connected_nodes)}
    else:
        peer_list = {'peers': (requester_url,)}
    db.set_connected_nodes(connected_nodes)
    return jsonify(peer_list)

def request_peers(url):
    '''
    Make a POST request to the url of another node
    to get its connected nodes
    The other node should return:
    {
        peers: list()
    }
    Args:
        url (str): URL of other node
    '''
    post_url = url + '/peers'
    own_address = db.get_own_address()
    response = requests.post(post_url, json={'url': own_address})
    connected_nodes = response.json()['peers']
    db.set_connected_nodes(connected_nodes)
