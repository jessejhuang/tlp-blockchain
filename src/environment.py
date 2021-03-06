'''
Environment variables and configurations
'''
import random
import urllib3
from dotenv import dotenv_values

FLASKENV_VARIABLES = dotenv_values(stream='.flaskenv')
PORT = FLASKENV_VARIABLES['FLASK_RUN_PORT']
HOST = FLASKENV_VARIABLES['FLASK_RUN_HOST']
ORIGIN_NODES = ('67.205.135.0',)
ORIGIN_IP = random.choice(ORIGIN_NODES)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
