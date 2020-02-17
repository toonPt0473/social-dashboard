from flask_restful import Resource
from flask import request
import pika
import json

class Controller(Resource):
  def get(self):
    print(1111)
    return
  def post(self):
    body = request.get_json(force=True)
    body = json.loads(body)
    print(body['label'])
    f = open("analyze_data.json", "r")
    analyze_data = json.load(f)
    f.close()

    analyze_data = { **analyze_data[body['label']], **body['data'] }
    f = open("analyze_data.json", "w")
    f.write(json.dumps(analyze_data))
    f.close()
    return