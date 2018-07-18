'''
Testing script to send request to flask server
'''
import requests

def request_server():
    '''
    Send whatever needed GET request
    '''
    send_dict = {'question':'what is the answer?'}
    res = requests.post('http://0.0.0.0:5000/address', json=send_dict)
    print('response from server:', res.text)
    recieve_dict = res.json()
    print('recieve dict: ', recieve_dict)

if __name__ == '__main__':
    request_server()
