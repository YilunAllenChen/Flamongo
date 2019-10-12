from flask import request, Flask, Response
from flask_cors import CORS

import json
from utils import *

class Server:

    def __init__(self):
        try:
            self.app = Flask(__name__)
            # For Local Testing Only
            CORS(self.app)
            print('Flask initialized successfully.')
        except:
            print('Failed to initialize Flask.')

        from flask_mongo import Mongo
        self.mongo = Mongo(self.app)
        
        from flask_kafka import Kafka
        self.kafka = Kafka(self.app)
