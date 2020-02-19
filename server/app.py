from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import sys
import os
import pika

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from controller import data, analyze

app = Flask(__name__)
CORS(app)
api = Api(app, prefix='/api')

api.add_resource(data.Controller, '/data', endpoint='data')
api.add_resource(analyze.Controller, '/analyze', endpoint='analyze')

if __name__ == "__main__":
  app.run(debug=True, port=3000, host="0.0.0.0")
