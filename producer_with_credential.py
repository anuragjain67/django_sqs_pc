import json
from boto.sqs.connection import SQSConnection
from sqs_exceptions import MissingCredential, ConnectionError,\
    QueueNotExists

def get_credentials():
    try:
        from django.conf import settings
        AWS_CREDENTIAL = settings.AWS_CREDENTIAL
        aws_sqs_queue_name = settings.SQS_QUEUE_NAME 
        aws_access_key = AWS_CREDENTIAL["aws_access_key"]
        aws_secret_key = AWS_CREDENTIAL["aws_secret_key"]
        return aws_access_key, aws_secret_key, aws_sqs_queue_name
    except:
        MissingCredential("Credential is not provided by User")

def get_sqs_connection(aws_access_key, aws_secret_key):
    try: 
        conn = SQSConnection(aws_access_key,aws_secret_key)    
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

aws_access_key, aws_secret_key, aws_sqs_queue_name = get_credentials()
conn = get_sqs_connection(aws_access_key, aws_secret_key)
q = get_queue(conn,aws_sqs_queue_name)
producer = django_sqs_producer(conn,q)
