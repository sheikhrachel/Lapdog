"""test module for lapdog class"""
import sys
sys.path.append("/Users/isaacsheikh/Document/GitHub/lapdog/src")
from lapdog import Lapdog
from conftest import *
import json

@mock_sqs
def test_lapdog_how_many_empty(sqs):
    bucket_name = 'test_bucket'
    queue_name = 'test_queue'
    resp = sqs.create_queue(QueueName=queue_name)
    queue_url = resp["QueueUrl"]

    response = sqs.get_queue_attributes(QueueUrl=queue_url)
    aws_number_of_messages = response['Attributes']["ApproximateNumberOfMessages"]
    
    lapdog_instance = Lapdog(bucket_name, queue_name, queue_url)
    lapdog_number_of_messages = lapdog_instance.how_many()
    
    assert lapdog_number_of_messages == aws_number_of_messages


@mock_sqs
def test_lapdog_how_many_five(sqs):
    bucket_name = 'test_bucket'
    queue_name = 'test_queue'
    resp = sqs.create_queue(QueueName=queue_name)
    queue_url = resp["QueueUrl"]

    test_messages = ['1', '2', '3', '4', '5']
    for message in test_messages:
        sqs.send_message(QueueUrl=queue_url, MessageBody=message)

    response = sqs.get_queue_attributes(QueueUrl=queue_url)
    aws_number_of_messages = response['Attributes']["ApproximateNumberOfMessages"]
    
    lapdog_instance = Lapdog(bucket_name, queue_name, queue_url)
    lapdog_number_of_messages = lapdog_instance.how_many()
    
    assert lapdog_number_of_messages == aws_number_of_messages


@mock_sqs
def test_lapdog_grab_issue(sqs):
    bucket_name = 'test_bucket'
    queue_name = 'test_queue'
    resp = sqs.create_queue(QueueName=queue_name)
    queue_url = resp["QueueUrl"]

    lapdog_instance = Lapdog(bucket_name, queue_name, queue_url)
    lapdog_instance.grab_issue()

    body = s3.Object(bucket_name, "steve").get()["Body"].read().decode("utf-8")
    assert body == "is awesome"


# @mock_s3
# def test_lapdog_complete_issue(s3, sqs):
#     s3.create_bucket(Bucket="test_bucket")
#     queue_name = "test_queue"
#     queue_url = sqs.create_queue(QueueName=queue_name)["QueueUrl"]

#     lapdog_instance = Lapdog(bucket_name, queue_name, queue_url)
#     lapdog_instance.complete_issue(receipt_handle, issue_id, report_body)

#     body = s3.Object("test_bucket", "steve").get()["Body"].read().decode("utf-8")
#     assert body == "is awesome"


# @mock_s3
# def test_lapdog_submit_issue(sqs):
#     queue_name = "test_queue"
#     queue_url = sqs.create_queue(QueueName=queue_name)["QueueUrl"]

#     lapdog_instance = Lapdog(bucket_name, queue_name, queue_url)
#     lapdog_instance.submit_issue()

#     body = s3.Object("test_bucket", "steve").get()["Body"].read().decode("utf-8")
#     assert body == "is awesome"
