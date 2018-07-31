'''
    Manage app variables through sqlite database to
    keep app.py as stateless as possible
'''
import sqlite3
import requests
from environment import ORIGIN_IP, PORT
from blockchain.node import Node

SESSION = {}

def setup_db():
    '''
    Create new tables
    '''
    connection = sqlite3.connect('blockchain.db')
    cur = connection.cursor()
    cur.execute('DROP TABLE IF EXISTS network')
    cur.execute('''
        CREATE TABLE network(
            address TEXT PRIMARY KEY
        )
    ''')

    cur.execute('DROP TABLE IF EXISTS local')
    cur.execute('''
        CREATE TABLE local(
            own_address TEXT
        )
    ''')
    connection.commit()
    connection.close()

def get_own_address():
    '''
    Returns:
        str: Address of own flask server
    '''
    connection = sqlite3.connect('blockchain.db')
    cur = connection.cursor()
    cur.execute('SELECT own_address FROM local')
    own_address = cur.fetchone()
    connection.close()
    if own_address is None:
        address = requests.get('https://enabledns.com/ip', verify=False).text #portless IP
        if address in ORIGIN_IP:
            print('This is the origin url')
            address = 'http://{}:{}'.format(address, PORT)
        else:
            res = requests.get('http://localhost:4040/api/tunnels') #get ngrok URL
            address = res.json()['tunnels'][0]['public_url']
        set_own_address(address)
        set_connected_nodes([address])
        return address
    return own_address[0]

def set_own_address(own_address):
    '''
    Sets own address
    '''
    connection = sqlite3.connect('blockchain.db')
    cur = connection.cursor()
    cur.execute('''
         INSERT OR REPLACE INTO local(own_address) values(?)
    ''', (own_address,))
    connection.commit()
    connection.close()

def get_connected_nodes():
    '''
    Returns:
        list() of str: urls of all discovered nodes
    '''
    connection = sqlite3.connect('blockchain.db')
    cur = connection.cursor()
    cur.execute('SELECT address FROM network')
    connected_node_tups = cur.fetchall()
    if connected_node_tups is None:
        return None
    connected_nodes = [tup[0] for tup in connected_node_tups]
    return connected_nodes

def set_connected_nodes(addresses):
    '''
    Updates network table with list of addresses
    '''
    connection = sqlite3.connect('blockchain.db')
    cur = connection.cursor()
    stmt = 'INSERT OR IGNORE INTO network(address) VALUES(?)'
    data = [(address,) for address in addresses]
    cur.executemany(stmt, data)
    connection.commit()
    connection.close()

def get_node():
    '''
    Get node object tracked by flask instance
    '''
    node = SESSION.get('node')
    if node is None:
        node = Node()
    node.peers = list(get_connected_nodes())
    set_node(node)
    return node

def set_node(node):
    '''
    Set node object tracked by flask instance
    '''
    SESSION['node'] = node
