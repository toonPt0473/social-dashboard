import requests
import json

def send_analyze_result(data):
  try:
    url = 'http://server:3000/api/analyze'
    data = json.dumps(data)
    requests.post(url, json = data)
  except:
    raise ValueError('request to api error')
  

