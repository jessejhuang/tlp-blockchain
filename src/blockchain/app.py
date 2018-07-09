'''
Flask Server

Manages a single node object and handles incoming requests from other nodes
'''
from flask import Flask, g, request
from node import Node

app = Flask(__name__)

# @app.before_first_request
def connect_to_network():
    '''
    Get the origin node's peers
    '''
    origin_url = 'http://174.138.127.161:5000'
    print("FOOOO")
    node = get_node()
    if str(request.base_url) != origin_url:
        node.request_peers(origin_url)
        print("BAR")
        set_node(node)


@app.route('/peers', methods=['POST'])
def send_peers():
    '''
    Returns:
        list(str) of urls of currently connected nodes
    '''
    node = get_node()
    input_json = request.get_json(force=True)
    requester_url = input_json.get('url')
    if requester_url:
        node.peers.append(requester_url)
    if node.peers[:-1]: # If len(peers not including requester) > 1
        return node.peers
    return request.remote_addr
    # return "No other nodes are connected."

def get_node():
    '''
    Get node object tracked by flask instance
    '''
    node = getattr(g, '_node', None)
    if node is None:
        node = g._node = Node()
    return node

def set_node(node):
    '''
    Set node object tracked by flask instance
    '''
    setattr(g, '_node', node)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
