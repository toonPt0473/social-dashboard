import pika
import time
import json
import pandas as pd
import re
import os
from datetime import datetime
from downloadfile import download_file_from_google_drive
from send_result import send_analyze_result
import logging

logger = logging.Logger('catch_all')

time.sleep(10)
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue='addNewCsv')

def generate_dataframe_from_file(filename):
  type_word = ['tweet', 'post', 'comment', 'reply', 'reply-comment', 'reply-reply-comment', 'news']
  def repl_func_start_content(matchobj):
      return f'''""'''
  def repl_func_end_content(matchobj):
      return f'"{matchobj.group()}'
  def repl_func_quote(matchobj):
      return f'""'
  def repl_func_content_comma(matchobj):
      return matchobj.group().replace(',', '')
  def repl_func_name(matchobj):
      text = matchobj.group().split(',')
      return text[0] + ',"' + ','.join(text[1:]) + '"'
  def repl_func_newline_content(matchobj):
      return re.sub(r'''\n''', '${newline}', matchobj.group())

  if (os.path.exists('newdata.csv')):
    os.remove("newdata.csv")
  w = open("newdata.csv", "a+")
  with open(filename) as infile:
    for line in infile:
      line = re.sub(r'''"''', repl_func_quote, line)
      line = re.sub(r"""'""", repl_func_quote, line)
      for t in type_word:
          start_message_regex = r',' + t + r','
          line = re.sub(start_message_regex, f',{t},"', line)
      line = re.sub(r''',\d{4}-\d{2}-\d{1,2}\s\d{2}:\d{2}:\d{2}''', repl_func_end_content, line)
      line = re.sub(r'(?<=,twitter,)(.*)(?=\n)', repl_func_name, line)
      line = re.sub(r'(?<=,facebook,)(.*)(?=\n)', repl_func_name, line)
      line = re.sub(r'(?<=,website,)(.*)(?=\n)', repl_func_name, line)
      line = re.sub(r'(?<=,instagram,)(.*)(?=\n)', repl_func_name, line)
      line = re.sub(r'(?<=,youtube,)(.*)(?=\n)', repl_func_name, line)
      line = re.sub(r'(?<=,pantip,)(.*)(?=\n)', repl_func_name, line)
      w.write(line)
  w.close()
  print('===============================================')
  f = open('newdata.csv')
  contents = f.read()
  f.close()
  contents = re.sub(r'''"([^"]*)"''', repl_func_newline_content, contents)
  f = open('newdata.csv', 'w')
  f.write(contents)
  f.close()
  print('end')
  return 


def callback(ch, method, properties, body):
  body = json.loads(body)
  print(body['g_drive_id'])
  try:
    if (os.path.exists('raw.csv')):
      os.remove("raw.csv")
    destination = 'raw.csv'
    download_file_from_google_drive(body['g_drive_id'], destination)
    print('download file success')
  except Exception as e:
    logger.error(str(e))
    data = {
      'label': body['label'],
      'data': {
        'pending': False,
        'error': True,
        'error_message': 'load file fail'
      }
    }
    send_analyze_result(data)
    return
  try:
    generate_dataframe_from_file(destination)
    csv = pd.read_csv('newdata.csv', error_bad_lines=False)
    # test 1
    date_df = pd.DataFrame()
    date_df['time'] = pd.to_datetime(csv['time']).dt.date
    date_df = pd.DataFrame(date_df.groupby(['time']).size()).reset_index()
    date_df = date_df.rename(columns={0 : 'date_count'})
    date_df = date_df.values.tolist()
    def myconverter(o):
      return o.__str__()
    daily_message = json.dumps(date_df, default = myconverter)

    # test 2
    top_messages_engagements = pd.DataFrame.from_records(data=csv, columns=['message', 'engagement'])
    top_messages_engagements = top_messages_engagements.sort_values(by='engagement', ascending=False)
    top_messages_engagements = top_messages_engagements.values.tolist()
    top_messages_engagements = top_messages_engagements[:10]

    # test 3
    top_accounts = pd.DataFrame.from_records(data=csv, columns=['owner id', 'owner name'])
    top_accounts = pd.DataFrame(top_accounts.groupby(['owner id', 'owner name']).size()).reset_index()
    top_accounts = top_accounts.rename(columns={0 : 'id_count'})
    top_accounts = top_accounts.sort_values(by='id_count', ascending=False)
    top_accounts = top_accounts.values.tolist()
    top_accounts = top_accounts[:10]
    data = {
      'label': body['label'],
      'data': {
        'pending': False,
        'data': {
          'daily_message': daily_message,
          'top_messages_engagements': top_messages_engagements,
          'top_accounts': top_accounts
        }
      }
    }
    send_analyze_result(data)
  except Exception as e:
    logger.error(str(e))
    data = {
      'label': body['label'],
      'data': {
        'pending': False,
        'error': True,
        'error_message': 'maybe csv is wrong format or file not found'
      }
    }
    send_analyze_result(data)
    return
  return 


channel.basic_consume(queue='addNewCsv', on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()
