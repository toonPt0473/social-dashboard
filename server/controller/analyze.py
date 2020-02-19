from flask_restful import Resource
from flask import request
import pika
import json

class Controller(Resource):
  def get(self):
    f = open("analyze_data.json", "r")
    analyze_data = json.load(f)
    f.close()
    return analyze_data
  def post(self):
    body = request.get_json(force=True)
    body = json.loads(body)
    f = open("analyze_data.json", "r")
    analyze_data = json.load(f)
    f.close()

    analyze_data[body['label']] = { **analyze_data[body['label']], **body['data'] }
    with open('analyze_data.json', 'w', encoding='utf8') as json_file:
      json.dump(analyze_data, json_file, ensure_ascii=False)
    # f = open("analyze_data.json", "w")
    # f.write(analyze_data)
    # f.close()
    return