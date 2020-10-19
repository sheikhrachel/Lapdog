"""Instance handler for slash command operations."""
import boto3
from config import BUCKET_NAME, QUEUE_NAME, SQS_QUEUE_URL


class Lapdog(object):
    """Instance handler for slash command operations."""

    def __init__(self, bucket_name, queue_name, queue_url):
        """Init method."""
        self.bucket_name = bucket_name
        self.queue_name = queue_name
        self.queue_url = queue_url

    def how_many(self):
        """Return current number of issues waiting in queue."""
        sqs = boto3.client('sqs', region_name='us-east-1')
        response = sqs.get_queue_attributes(QueueUrl=self.queue_url)
        return response["Attributes"]["ApproximateNumberOfMessages"]

    def grab_issue(self):
        """Return an issue from queue."""
        sqs = boto3.resource('sqs', region_name='us-east-1')
        response = sqs.receive_message(QueueUrl=SQS_QUEUE_URL,
                                       AttributeNames=['SentTimestamp'])
        message = response['Messages'][0]
        body = message['Body']
        receipt_handle = message['ReceiptHandle']
        issue_id = message['Messages']['MessageId']
        return [body, receipt_handle, issue_id]

    def complete_issue(self, receipt_handle, issue_id, report_body):
        """Mark issue as complete, log record in S3, and delete from queue."""
        s3 = boto3.client('s3', region_name='us-east-1')
        sqs = boto3.resource('sqs', region_name='us-east-1')
        queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)
        queue.delete_message(QueueUrl=SQS_QUEUE_URL,
                             ReceiptHandle=receipt_handle)
        s3.put_object(Bucket=BUCKET_NAME, Key=issue_id, Body=report_body)

    def submit_issue(self, priority, submitter, assignee, issue_body):
        """Create new issue, and submit to queue."""
        sqs = boto3.resource('sqs', region_name='us-east-1')
        queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)
        message_attributes = {'Submitter': {'DataType': 'String',
                                            'StringValue': submitter},
                              'Assignee': {'DataType': 'String',
                                           'StringValue': assignee}}
        queue.send_message(MessageAttributes=message_attributes,
                           MessageBody=(issue_body))
