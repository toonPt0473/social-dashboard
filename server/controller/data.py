from flask_restful import Resource
from flask import request
import pika


class Controller(Resource):
  # def __init__(self):
  def post(self):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
    print(" [x] Sent 'Hello World!'")
    connection.close()
    json_data = request.get_json(force=True)
    print(json_data)
    return 
