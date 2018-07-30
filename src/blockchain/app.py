'''
Flask Server

Manages a single node object and handles incoming requests from other nodes
'''
import random
import threading
import time
import requests
from dotenv import dotenv_values
from flask import Flask, g, request, jsonify
from node import Node
from block import Block
import json

FLASKENV_VARIABLES = dotenv_values(stream='.flaskenv')
PORT = FLASKENV_VARIABLES['FLASK_RUN_PORT']
HOST = FLASKENV_VARIABLES['FLASK_RUN_HOST']
ORIGIN_NODES = ('67.205.135.0',)
ORIGIN_IP = random.choice(ORIGIN_NODES)

SESSION = {} # Store flask variables such as address, node

def start_runner():
    '''
    https://networklore.com/start-task-with-flask/
    '''
    def start_loop():
        '''
        Triggers before_first_request
        Create thread to send get request to home every 2 seconds
        until a valid response is returned
        '''
        not_started = True
        while not_started:
            try:
                req = requests.get('http://{}:{}'.format(HOST, PORT))
                if req.status_code == 200:
                    print('Server started')
                    return # Closes thread
            except (ConnectionRefusedError, requests.exceptions.ConnectionError):
                print('Server not yet started')
            time.sleep(2)
    thread = threading.Thread(target=start_loop)
    thread.start()

def create_app():
    '''
    Call start_runner before app.run()
    '''
    start_runner()
    application = Flask(__name__)
    return application

app = create_app()

@app.before_first_request
def connect_to_network():
    '''
    On startup, get peers of the origin url
    '''
    address = get_own_address()
    if ORIGIN_IP not in address:
        request_peers('http://{}:{}'.format(ORIGIN_IP, PORT))
    node = get_node()
    print('Peers: ', node.peers)

def get_own_address():
    '''
    If on localhost with ngrok, get generated url
    else get flask.request.base_url
    '''
    if SESSION.get('address') is None:
        node = get_node()
        address = requests.get('https://enabledns.com/ip', verify=False).text #portless IP
        if address in ORIGIN_IP:
            print('This is the origin url')
            address = 'https://{}:{}'.format(address, PORT)
        else:
            res = requests.get('http://localhost:4040/api/tunnels') #get ngrok URL
            address = res.json()['tunnels'][0]['public_url']
        SESSION['address'] = address
        node.peers.append(address)
    address = SESSION['address']
    return address

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
    own_address = get_own_address()
    print(post_url, own_address)
    response = requests.post(post_url, json={'url': own_address})
    node = get_node()
    node.peers = response.json()['peers']
    node.peers.append('http://7f3f6de4.ngrok.io')
    set_node(node)

@app.route('/')
def welcome():
    '''
    homepage
    '''
    return 'TODO: Implement Visualization'

@app.route('/print',methods=['GET'])
def test():
    '''
    allows us to see the chain, peers and last hash of the nodes blockchain
    '''
    node = get_node()
    #b = Block(node.last_hash)
    #node.add_block(b,node.peers)
    data = "Chain: {}\nPeers: {}\n\nLast Hash: {}".format(str(node.chain), str(node.peers), node.last_hash)
    #return data

    json = {"Chain": node.chain, "Peers": node.peers, "Last Hash": node.last_hash}
    return jsonify(chain=node.chain,
                   peers=node.peers,
                   last_hash=node.last_hash
                   )

@app.route('/add', methods=['POST'])
def receiveBlock():
    '''
    allows node to receive new blocks from user to share to network and begin validation
    '''
    node = get_node()
    new_block_data = request.get_json()


    new_block = Block(node.last_hash, new_block_data['block']['check_number'], new_block_data['block']['sender'], new_block_data['block']['recipient'], new_block_data['block']['amount'])



    node.share_block(new_block, new_block_data, get_own_address())
    node.add_block(new_block, get_own_address())

    data = "New Block Pending: Sender: {}\nRecipient: {}\nAmount: {}".format(str(new_block_data['block']['sender']), str(new_block_data['block']['recipient']), new_block_data['block']['amount'])
    return data

@app.route('/halt', methods=['POST'])
def updateChain():
    '''
    allows node to receive validated block from other nodes
    '''
    node = get_node()
    new_block_data = request.get_json()
    hash = ""
    try:
        hash = new_block_data['hash']
        print(hash)
    except:
        pass


    new_Block = Block(node.last_hash, new_block_data['check_number'], new_block_data['sender'], new_block_data['recipient'], new_block_data['amount'])
    new_Block.hash = hash
    node.chain.append(json.dumps(new_Block.__dict__))
    #b = Block(node.last_hash)
    #node.add_block(b,node.peers)
    data = "New Block added to chain: Sender: {}\nRecipient: {}\nAmount: {}".format(str(new_block_data['sender']), str(new_block_data['recipient']), new_block_data['amount'])
    return data

@app.route('/address', methods=['POST'])
def send_client_address():
    '''
    Return a client's address
    '''

    return jsonify({'address': request.remote_addr})

@app.route('/peers', methods=['POST'])
def send_peers():
    '''
    Input json:
        {
            url: requester_url
        }
    Returns:
        list(str) of urls of currently connected nodes
    '''
    node = get_node()
    input_json = request.get_json(force=True)
    requester_url = input_json.get('url')
    if requester_url and requester_url not in node.peers:
        node.peers.append(requester_url)
    if node.peers[:-1]: # If len(peers not including requester) > 1
        peers = {'peers': tuple(node.peers)}
    else:
        peers = {'peers': (requester_url,)}
    print('Node.peers: ', node.peers)
    print('Node.peers[:-1]: ', node.peers[:-1])
    set_node(node)
    return jsonify(peers)

def get_node():
    '''
    Get node object tracked by flask instance
    '''
    node = SESSION.get('node')
    if node is None:
        node = Node()
        set_node(node)
    return node

def sendBlock(block, node_url):
    '''

    :param block: block to be sent to another node
    :param node_url: other node's url
    :return:
    '''
    block = {'new_block': request.json['new_block']}

def set_node(node):
    '''
    Set node object tracked by flask instance
    '''
    SESSION['node'] = node

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)

