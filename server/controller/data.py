from flask_restful import Resource
from flask import request
import pika
import json
import time

class Controller(Resource):
  def post(self):
    body = request.get_json()
    f = open("analyze_data.json", "r")
    analyze_data = json.load(f)
    f.close()
    analyze_data[body['label'] + str(round(time.time() * 1000))] = {
      'pending': True,
      'title': body['label'],
      'g_drive_id': body['g_drive_id']
    }
    with open('analyze_data.json', 'w', encoding='utf8') as json_file:
      json.dump(analyze_data, json_file, ensure_ascii=False)
    send_data = json.dumps({
      'label': body['label'] + str(round(time.time() * 1000)),
      'g_drive_id': body['g_drive_id']
    })
    print(send_data)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='addNewCsv')
    channel.basic_publish(exchange='', routing_key='addNewCsv', body=send_data)
    connection.close()