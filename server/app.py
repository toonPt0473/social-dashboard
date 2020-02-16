from flask import Flask
from flask_restful import Api
import sys
import os
import pika

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from controller import data

app = Flask(__name__)
api = Api(app, prefix='/api/')

api.add_resource(data.Controller, '/data')

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')


def callback(ch, method, properties, body):
  print(" [x] Received %r" % body)


channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

if __name__ == "__main__":
  app.run(debug=True, port=3000, host="0.0.0.0")
