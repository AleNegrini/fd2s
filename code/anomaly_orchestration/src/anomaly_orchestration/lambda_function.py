import boto3
import json
import time
from datetime import datetime, timedelta

from sqs_helper import sqs_helper
from utils import Utils

def lambda_handler(event, context):

    # setup S3 resource
    s3 = boto3.resource('s3')

    # Set up SQS clients
    sqs_ppg = sqs_helper(Utils.get_environment(key_name='TEMP_SQS_URL',
                                               default='https://sqs.eu-central-1.amazonaws.com/851479583999/empatica-sqs-model-x-temp'))
    sqs_temp = sqs_helper(Utils.get_environment(key_name='PPG_SQS_URL',
                                               default='https://sqs.eu-central-1.amazonaws.com/851479583999/empatica-sqs-model-x-ppg'))

    # retrieve the today value, passed via event
    today_str = event['time'][0:10].replace('-', '/')
    today = datetime.strptime(today_str, '%Y/%m/%d')
    yesterday = today - timedelta(days=1)

    # list the objects inside the bucket
    bucket_name = Utils.get_environment(key_name='BUCKET_NAME',
                                        default='empatica-model-x')
    bucket = s3.Bucket(bucket_name)
    devices = set()

    for my_bucket_object in bucket.objects.filter(Prefix=yesterday.strftime('%Y/%m/%d') + '/'):
        device_to_check = my_bucket_object.key
        device = device_to_check[11:21]
        devices.add(device)

    for item in devices:
        message = {
            'day': yesterday.strftime('%Y/%m/%d'),
            'device': item
        }

        sqs_temp.send_message(message_body=json.dumps(message))
        sqs_ppg.send_message(message_body=json.dumps(message))
        time.sleep(2)
