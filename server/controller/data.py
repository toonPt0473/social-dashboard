from flask_restful import Resource
from flask import request
import pika
import json

class Controller(Resource):
  def post(self):
    body = request.get_json()
    body = json.dumps(body)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='addNewCsv')
    channel.basic_publish(exchange='', routing_key='addNewCsv', body=body)
    connection.close()