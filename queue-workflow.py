import boto3
import logging
from botocore.exceptions import ClientError
import subprocess
from subprocess import call
import yaml
# import time


logger = logging.getLogger(__name__)

# Creating sqs client
sqs = boto3.client('sqs')

def create_queue(name, attributes=None):
    if not attributes:
        attributes = {}
    try:
        queue = sqs.create_queue(
            QueueName=name,
            Attributes=attributes
        )
        # logger.info("Created queue '%s' with URL=%s", name, queue.url)
    except ClientError as error:
        logger.exception("Is not possible create the queue '%s' ", name)
        raise error
    else:
        return queue

def creating_queues():
    prefix = 'test_devops_'
    file_name='./queues_definition-2.yml'
    with open(file_name) as f:
        doc = yaml.safe_load(f)

    # ######################################
    # Creating test_devops_makelaars queue #
    # ######################################
    queue1 = doc['sqs']['team1']['queue1']
    queue1_queue = create_queue(
        # prefix + 'makelaars',
        queue1,
        {
            'MaximumMessageSize': str(4096),
            'ReceiveMessageWaitTimeSeconds': str(20),
            'VisibilityTimeout': str(300),
        }
    )
    # response = sqs.get_queue_url(QueueName=prefix + 'makelaars')
    response = sqs.get_queue_url(QueueName=queue1)
    print('Name of the queue created: {}'.format(queue1))
    print('URL: {}'.format(response['QueueUrl']))
    sqsid = boto3.resource('sqs')
    queue = sqsid.get_queue_by_name(QueueName=queue1)

    url = queue.url
    print ("Sending messages to: {queue_name}".format(queue_name=queue1))

    # sending messages to the queue
    # rc = call("./send.sh")
    call(["./send.sh", str(url)])


    # #############################################
    # Creating test_devops_makelaars_errors queue #
    # #############################################
    queue2 = doc['sqs']['team1']['queue2']
    queue2_queue = create_queue(
        # prefix + 'makelaars_errors',
        queue2,
        {
            'MaximumMessageSize': str(4096),
            'ReceiveMessageWaitTimeSeconds': str(10),
            'VisibilityTimeout': str(300),
        }
    )
    response = sqs.get_queue_url(QueueName=queue2)
    print('Name of the queue created: {}'.format(queue2))
    print('URL: {}'.format(response['QueueUrl']))
    sqsid = boto3.resource('sqs')
    queue = sqsid.get_queue_by_name(QueueName=queue2)
    url = queue.url
    print ("Sending messages to: {queue_name}".format(queue_name=queue2))
    rc = call(["./send.sh", str(url)])



    # #############################################
    # Creating test_devops_new_houses queue #
    # #############################################
    queue3 = doc['sqs']['team2']['queue1']
    queue3_queue = create_queue(
        # prefix + 'makelaars_errors',
        queue3,
        {
            'MaximumMessageSize': str(4096),
            'ReceiveMessageWaitTimeSeconds': str(10),
            'VisibilityTimeout': str(300),
        }
    )
    response = sqs.get_queue_url(QueueName=queue3)
    print('Name of the queue created: {}'.format(queue3))
    print('URL: {}'.format(response['QueueUrl']))
    sqsid = boto3.resource('sqs')
    queue = sqsid.get_queue_by_name(QueueName=queue3)
    url = queue.url
    print ("Sending messages to: {queue_name}".format(queue_name=queue3))
    rc = call(["./send.sh", str(url)])


    # #############################################
    # Creating test_devops_new_houses_errors queue #
    # #############################################
    queue4 = doc['sqs']['team2']['queue2']
    queue4_queue = create_queue(
        # prefix + 'makelaars_errors',
        queue4,
        {
            'MaximumMessageSize': str(4096),
            'ReceiveMessageWaitTimeSeconds': str(10),
            'VisibilityTimeout': str(300),
        }
    )
    response = sqs.get_queue_url(QueueName=queue4)
    print('Name of the queue created: {}'.format(queue4))
    print('URL: {}'.format(response['QueueUrl']))
    sqsid = boto3.resource('sqs')
    queue = sqsid.get_queue_by_name(QueueName=queue4)
    url = queue.url
    print ("Sending messages to: {queue_name}".format(queue_name=queue4))
    rc = call(["./send.sh", str(url)])


def main():
    go = input("""
               By creating those queues and sending them messages
               you should use your default AWS account credentials and
               might incur charges on your account. \n
               Do you want to continue (y/n)?""")
    if go.lower() == 'y':
        print("Starting to create and send messages to the queue.")
        creating_queues()
    else:
        print("Good bye!")


if __name__ == '__main__':
    main()
