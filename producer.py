import json
import boto.sqs
from sqs_exceptions import MissingQueueName, ConnectionError,\
    QueueNotExists

def get_queue_name():
    try:
        from django.conf import settings
        aws_sqs_queue_name = settings.SQS_QUEUE_NAME 
        return aws_sqs_queue_name
    except:
        MissingQueueName("Queue name is missing in settings")

def get_sqs_connection():
    try: 
        from django.conf import settings
        REGION_NAME = settings.REGION_NAME
        conn = boto.sqs.connect_to_region(REGION_NAME)    
        return conn
    except:
        raise ConnectionError("Given Credential is wrong")

def get_queue(conn,aws_sqs_queue_name):
    q = conn.get_queue(aws_sqs_queue_name)
    if q:
        return q
    else:
        raise QueueNotExists("Given Queue name is not exists in your AWS Account") 

class django_sqs_producer(object):
    def __init__(self, conn, q):
        self.conn = conn
        self.q = q
    
    def run_async(self,task_name, params=None): 
        params = params or {}
        payload = {
                   "task_name":task_name,
                   "params": params
                   }
        payload_as_json = json.dumps(payload)
        self.conn.send_message(self.q,payload_as_json)

conn = get_sqs_connection()
aws_sqs_queue_name = get_queue_name()
q = get_queue(conn,aws_sqs_queue_name)
producer = django_sqs_producer(conn,q)
