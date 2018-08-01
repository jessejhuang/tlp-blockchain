'''
Flask Server

Manages a single node object and handles incoming requests from other nodes

Usage: flask run
'''
import threading
import time
import requests
from flask import Flask
import database as db
from environment import ORIGIN_IP, PORT, HOST
from .blueprints.peers import peers, request_peers
from .blueprints.interface import interface

def start_runner():
    '''
    https://networklore.com/start-task-with-flask/
    '''
    def start_loop():
        '''
        Triggers before_first_request connect_to_network
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
    db.setup_db()
    start_runner()
    application = Flask(__name__)
    application.register_blueprint(peers)
    application.register_blueprint(interface)
    return application

app = create_app()

@app.before_first_request
def connect_to_network():
    '''
    On startup, get peers of the origin url
    '''
    address = db.get_own_address()
    if ORIGIN_IP not in address:
        request_peers('http://{}:{}'.format(ORIGIN_IP, PORT))
    connected_nodes = db.get_connected_nodes()
    print('Connected nodes: ', connected_nodes)


@app.route('/')
def welcome():
    '''
    homepage
    '''
    return 'TODO: Implement Visualization'
