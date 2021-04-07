import boto3
from typing import Dict

class dynamo_helper():
    """
    Helper class for DynamoDB
    """
    def _get_dynamo_client(self):
        try:
            return boto3.client('dynamodb')
        except Exception:
            print("An error occurred while setting up DynamoDB client")

    def __init__(self):
        self.client = self._get_dynamo_client()

    def put_item(self,
                 table_name: str,
                 item: Dict):
        """
        Put item in the passed DynamoDB table
        :param table_name: DynamoDB table
        :param item: item to put
        """
        try:
            self.client.put_item(TableName=table_name,
                                 Item=item)
            print("Item "+str(item)+" successfully written on the dynamoDB table "+table_name)
        except:
            print("An error occurred while writing " + str(item) + " on the dynamoDB table " + table_name)