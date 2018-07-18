'''
Flask Server

Manages a single node object and handles incoming requests from other nodes
'''
import threading
import time
import requests
from flask import Flask, g, request, jsonify
from node import Node

ORIGIN_IP = '67.205.135.0:5000'

def start_runner():
    '''
    https://networklore.com/start-task-with-flask/
    '''
    def start_loop():
        '''
        Triggers before_first_request
        Create thread to get send get request to home every 2 seconds
        until a valid response is returned
        '''
        not_started = True
        while not_started:
            try:
                req = requests.get('http://0.0.0.0:5000/')
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
    application = Flask(__name__)
    start_runner()
    return application

app = create_app()

@app.before_first_request
def connect_to_network():
    '''
    On startup, get peers of the origin url
    '''
    address = get_own_address()
    if ORIGIN_IP not in address:
        request_peers('http://' + ORIGIN_IP)
    node = get_node()
    print('Peers: ', node.peers)

def get_own_address():
    '''
    If on localhost with ngrok, get generated url
    else get flask.request.base_url
    '''
    if 'address' not in g:
        address = requests.get('https://enabledns.com/ip', verify=False).text #portless IP
        if address in ORIGIN_IP:
            print('The origin url')
            setattr(g, 'address', ORIGIN_IP)
        else:
            res = requests.get('http://localhost:4040/api/tunnels')
            address = res.json()['tunnels'][0]['public_url']
            setattr(g, 'address', address)
    address = getattr(g, 'address', None)
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
    response = requests.post(post_url, json={'url': own_address})
    node = get_node()
    node.peers = response.json()['peers']
    set_node(node)

@app.route('/')
def welcome():
    '''
    homepage
    '''
    return 'TODO: Implement Visualization'


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
    if requester_url:
        node.peers.append(requester_url)
    if node.peers[:-1]: # If len(peers not including requester) > 1
        peers = {'peers': tuple(node.peers)}
    else:
        peers = {'peers': (requester_url,)}
    set_node(node)
    print('peers: ', peers)
    return jsonify(peers)

def get_node():
    '''
    Get node object tracked by flask instance
    '''
    node = getattr(g, 'node', None)
    if node is None:
        node = g.node = Node()
    return node

def set_node(node):
    '''
    Set node object tracked by flask instance
    '''
    setattr(g, 'node', node)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
