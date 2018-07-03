from flask import Flask, g, jsonify, render_template, request, url_for
from node import Node

app = Flask(__name__)

@app.before_first_request
def connect_to_network():
    """ Get the origin node's peers"""
    origin_url = 'http://174.138.127.161:5000'
    print("FOOOO")
    node = getNode()
    if str(request.base_url) != origin_url:
        node.request_peers(origin_url)
        print("BAR")
        setNode(node)


@app.route('/peers', methods=['POST'])
def send_peers():
    node = getNode()
    if len(node.peers) > 0:
        return node.peers
    else:
        return "No other nodes are connected."

def getNode():
    node = getattr(g, '_node', None)
    if node is None:
        node = g._node = Node(0)
    return node

def setNode(node):
    g._node = node 

if __name__ == "__main__":
    app.run(host='0.0.0.0')
