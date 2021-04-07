import boto3

class sqs_helper():
    """
    Helper class for SQS queue management
    """

    def _get_sqs_client(self):
        try:
            return boto3.client('sqs')
        except Exception:
            print("An error occurred while setting up SQS client")

    def __init__(self, queue_name: str):
        self.queue_name = queue_name
        self.client = self._get_sqs_client()

    def send_message(self, message_body, message_attributes=None):
        """
        Send a message to an Amazon SQS queue.

        Usage is shown in usage_demo at the end of this module.

        :param message_body: The body text of the message.
        :param message_attributes: Custom attributes of the message. These are key-value
                                   pairs that can be whatever you want.
        :return: The response from SQS that contains the assigned message ID.
        """
        if not message_attributes:
            message_attributes = {}

        try:
            response = self.client.send_message(
                QueueUrl=self.queue_name,
                MessageBody=message_body,
                MessageAttributes=message_attributes
            )
            print("Send message success on queue " + self.queue_name + " :" + message_body)
        except Exception as error:
            print("Send message failed on queue " + self.queue_name + " :" + message_body)
            raise error
        else:
            return response
