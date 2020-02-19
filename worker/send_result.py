import requests
import json

def send_analyze_result(data):
  url = 'http://server:3000/api/analyze'
  data = json.dumps(data)
  requests.post(url, json = data)
  return
  

