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
# prefix = 'test_devops_'
# Reading file definition
file_name='./queues_definition-2.yml'
with open(file_name) as f:
        doc = yaml.safe_load(f)

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

def test_devops_makelaars():

    welcome = """
    # ######################################
    # Creating test_devops_makelaars queue #
    # ######################################
    """
    print (welcome)
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

    go = input("""
               Do you want to send messages to {queue_name} (y/n)?""".format(queue_name=queue1))
    if go.lower() == 'y':
        print ("Sending messages to: {queue_name}".format(queue_name=queue1))

        # sending messages to the queue
        # rc = call("./send.sh")
        call(["./sending-batch-messages.sh", str(url)])
    else:
        print("Please continue with other queues. Good bye!")

def test_devops_makelaars_errors():

    welcome = """
    # #############################################
    # Creating test_devops_makelaars_errors queue #
    # #############################################
    """
    print (welcome)

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

    go = input("""
               Do you want to send messages to {queue_name} (y/n)?""".format(queue_name=queue2))
    if go.lower() == 'y':
        file_error = 'send_errors.json'
        print ("Sending messages to: {queue_name}".format(queue_name=queue2))
        rc = call(["./sending_error_msg_batch.sh", str(url), str(file_error)])
    else:
        print("Please continue with other queues. Good bye!")

def test_devops_new_houses():
    welcome = """
    # #######################################
    # Creating test_devops_new_houses queue #
    # #######################################
    """
    print (welcome)

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
    go = input("""
               Do you want to send messages to {queue_name} (y/n)?""".format(queue_name=queue3))
    if go.lower() == 'y':
        print ("Sending messages to: {queue_name}".format(queue_name=queue3))
        rc = call(["./sending-batch-messages.sh", str(url)])
    else:
        print("Please continue with other queues. Good bye!")

def test_devops_new_houses_errors():
    welcome = """
    # ##############################################
    # Creating test_devops_new_houses_errors queue #
    # ##############################################
    """
    print (welcome)

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

    go = input("""
               Do you want to send messages to {queue_name} (y/n)?""".format(queue_name=queue4))
    if go.lower() == 'y':
        file_error = 'send_errors.json'
        print ("Sending messages to: {queue_name}".format(queue_name=queue4))
        rc = call(["./sending_error_msg_batch.sh", str(url), str(file_error)])
    else:
        print("Please continue with other queues. Good bye!")

def test_devops_edited_houses():
    welcome = """
    # ##########################################
    # Creating test_devops_edited_houses queue #
    # ##########################################
    """
    print (welcome)
    queue5 = doc['sqs']['team2']['queue3']
    queue5_queue = create_queue(
        # prefix + 'makelaars_errors',
        queue5,
        {
            'MaximumMessageSize': str(4096),
            'ReceiveMessageWaitTimeSeconds': str(10),
            'VisibilityTimeout': str(300),
        }
    )
    response = sqs.get_queue_url(QueueName=queue5)
    print('Name of the queue created: {}'.format(queue5))
    print('URL: {}'.format(response['QueueUrl']))
    sqsid = boto3.resource('sqs')
    queue = sqsid.get_queue_by_name(QueueName=queue5)
    url = queue.url
    go = input("""
               Do you want to send messages to {queue_name} (y/n)?""".format(queue_name=queue5))
    if go.lower() == 'y':
        print ("Sending messages to: {queue_name}".format(queue_name=queue5))
        rc = call(["./sending-batch-messages.sh", str(url)])
    else:
        print("Please continue with other queues. Good bye!")

def test_devops_edited_houses_errors():
    welcome = """
    # #################################################
    # Creating test_devops_edited_houses_errors queue #
    # #################################################
    """
    print (welcome)

    queue6 = doc['sqs']['team2']['queue4']
    queue6_queue = create_queue(
        # prefix + 'makelaars_errors',
        queue6,
        {
            'MaximumMessageSize': str(4096),
            'ReceiveMessageWaitTimeSeconds': str(10),
            'VisibilityTimeout': str(300),
        }
    )
    response = sqs.get_queue_url(QueueName=queue6)
    print('Name of the queue created: {}'.format(queue6))
    print('URL: {}'.format(response['QueueUrl']))
    sqsid = boto3.resource('sqs')
    queue = sqsid.get_queue_by_name(QueueName=queue6)
    url = queue.url

    go = input("""
               Do you want to send messages to {queue_name} (y/n)?""".format(queue_name=queue6))
    if go.lower() == 'y':
        file_error = 'send_errors.json'
        print ("Sending messages to: {queue_name}".format(queue_name=queue6))
        rc = call(["./sending_error_msg_batch.sh", str(url), str(file_error)])
    else:
        print("Please continue with other queues. Good bye!")

def test_devops_removed_houses():
    welcome = """
    # ###########################################
    # Creating test_devops_removed_houses queue #
    # ###########################################
    """
    print (welcome)
    queue7 = doc['sqs']['team2']['queue5']
    queue7_queue = create_queue(
        # prefix + 'makelaars_errors',
        queue7,
        {
            'MaximumMessageSize': str(4096),
            'ReceiveMessageWaitTimeSeconds': str(10),
            'VisibilityTimeout': str(300),
        }
    )
    response = sqs.get_queue_url(QueueName=queue7)
    print('Name of the queue created: {}'.format(queue7))
    print('URL: {}'.format(response['QueueUrl']))
    sqsid = boto3.resource('sqs')
    queue = sqsid.get_queue_by_name(QueueName=queue7)
    url = queue.url
    go = input("""
               Do you want to send messages to {queue_name} (y/n)?""".format(queue_name=queue7))
    if go.lower() == 'y':
        print ("Sending messages to: {queue_name}".format(queue_name=queue7))
        rc = call(["./sending-batch-messages.sh", str(url)])
    else:
        print("Please continue with other queues. Good bye!")

def test_devops_removed_houses_errors():
    welcome = """
    # ##################################################
    # Creating test_devops_removed_houses_errors queue #
    # ##################################################
    """
    print (welcome)

    queue8 = doc['sqs']['team2']['queue6']
    queue8_queue = create_queue(
        # prefix + 'makelaars_errors',
        queue8,
        {
            'MaximumMessageSize': str(4096),
            'ReceiveMessageWaitTimeSeconds': str(10),
            'VisibilityTimeout': str(300),
        }
    )
    response = sqs.get_queue_url(QueueName=queue8)
    print('Name of the queue created: {}'.format(queue8))
    print('URL: {}'.format(response['QueueUrl']))
    sqsid = boto3.resource('sqs')
    queue = sqsid.get_queue_by_name(QueueName=queue8)
    url = queue.url

    go = input("""
               Do you want to send messages to {queue_name} (y/n)?""".format(queue_name=queue8))
    if go.lower() == 'y':
        file_error = 'send_errors.json'
        print ("Sending messages to: {queue_name}".format(queue_name=queue8))
        rc = call(["./sending_error_msg_batch.sh", str(url), str(file_error)])
    else:
        print("Please continue with other queues. Good bye!")

def test_devops_stats_phone_clicks():
    welcome = """
    # ###############################################
    # Creating test_devops_stats_phone_clicks queue #
    # ###############################################
    """
    print (welcome)
    queue9 = doc['sqs']['team3']['queue1']
    queue9_queue = create_queue(
        # prefix + 'makelaars_errors',
        queue9,
        {
            'MaximumMessageSize': str(4096),
            'ReceiveMessageWaitTimeSeconds': str(10),
            'VisibilityTimeout': str(300),
        }
    )
    response = sqs.get_queue_url(QueueName=queue9)
    print('Name of the queue created: {}'.format(queue9))
    print('URL: {}'.format(response['QueueUrl']))
    sqsid = boto3.resource('sqs')
    queue = sqsid.get_queue_by_name(QueueName=queue9)
    url = queue.url
    go = input("""
               Do you want to send messages to {queue_name} (y/n)?""".format(queue_name=queue9))
    if go.lower() == 'y':
        print ("Sending messages to: {queue_name}".format(queue_name=queue9))
        rc = call(["./sending-batch-messages.sh", str(url)])
    else:
        print("Please continue with other queues. Good bye!")

def test_devops_stats_phone_clicks_errors():
    welcome = """
    # ######################################################
    # Creating test_devops_stats_phone_clicks_errors queue #
    # ######################################################
    """
    print (welcome)

    queue10 = doc['sqs']['team3']['queue2']
    queue10_queue = create_queue(
        # prefix + 'makelaars_errors',
        queue10,
        {
            'MaximumMessageSize': str(4096),
            'ReceiveMessageWaitTimeSeconds': str(10),
            'VisibilityTimeout': str(300),
        }
    )
    response = sqs.get_queue_url(QueueName=queue10)
    print('Name of the queue created: {}'.format(queue10))
    print('URL: {}'.format(response['QueueUrl']))
    sqsid = boto3.resource('sqs')
    queue = sqsid.get_queue_by_name(QueueName=queue10)
    url = queue.url

    go = input("""
               Do you want to send messages to {queue_name} (y/n)?""".format(queue_name=queue10))
    if go.lower() == 'y':
        file_error = 'send_errors.json'
        print ("Sending messages to: {queue_name}".format(queue_name=queue10))
        rc = call(["./sending_error_msg_batch.sh", str(url), str(file_error)])
    else:
        print("Please continue with other queues. Good bye!")

def test_devops_stats_facebook_clicks():
    welcome = """
    # ##################################################
    # Creating test_devops_stats_facebook_clicks queue #
    # ##################################################
    """
    print (welcome)
    queue11 = doc['sqs']['team3']['queue3']
    queue11_queue = create_queue(
        # prefix + 'makelaars_errors',
        queue11,
        {
            'MaximumMessageSize': str(4096),
            'ReceiveMessageWaitTimeSeconds': str(10),
            'VisibilityTimeout': str(300),
        }
    )
    response = sqs.get_queue_url(QueueName=queue11)
    print('Name of the queue created: {}'.format(queue11))
    print('URL: {}'.format(response['QueueUrl']))
    sqsid = boto3.resource('sqs')
    queue = sqsid.get_queue_by_name(QueueName=queue11)
    url = queue.url
    go = input("""
               Do you want to send messages to {queue_name} (y/n)?""".format(queue_name=queue11))
    if go.lower() == 'y':
        print ("Sending messages to: {queue_name}".format(queue_name=queue11))
        rc = call(["./sending-batch-messages.sh", str(url)])
    else:
        print("Please continue with other queues. Good bye!")

def test_devops_stats_facebook_clicks_errors():
    welcome = """
    # #########################################################
    # Creating test_devops_stats_facebook_clicks_errors queue #
    # #########################################################
    """
    print (welcome)

    queue12 = doc['sqs']['team3']['queue4']
    queue12_queue = create_queue(
        # prefix + 'makelaars_errors',
        queue12,
        {
            'MaximumMessageSize': str(4096),
            'ReceiveMessageWaitTimeSeconds': str(10),
            'VisibilityTimeout': str(300),
        }
    )
    response = sqs.get_queue_url(QueueName=queue12)
    print('Name of the queue created: {}'.format(queue12))
    print('URL: {}'.format(response['QueueUrl']))
    sqsid = boto3.resource('sqs')
    queue = sqsid.get_queue_by_name(QueueName=queue12)
    url = queue.url

    go = input("""
               Do you want to send messages to {queue_name} (y/n)?""".format(queue_name=queue12))
    if go.lower() == 'y':
        file_error = 'send_errors.json'
        print ("Sending messages to: {queue_name}".format(queue_name=queue12))
        rc = call(["./sending_error_msg_batch.sh", str(url), str(file_error)])
    else:
        print("We've finished. Good bye!")

def main():
    go = input("""
               By creating those queues and sending them messages
               you should use your default AWS account credentials and
               might incur charges on your account. \n
               Do you want to continue (y/n)?""")
    if go.lower() == 'y':
        print("Starting to create all queues and send messages to them.")
        test_devops_makelaars()
        test_devops_makelaars_errors()
        test_devops_new_houses()
        test_devops_new_houses_errors()
        test_devops_edited_houses()
        test_devops_edited_houses_errors()
        test_devops_removed_houses()
        test_devops_removed_houses_errors()
        test_devops_stats_phone_clicks()
        test_devops_stats_phone_clicks_errors()
        test_devops_stats_facebook_clicks()
        test_devops_stats_facebook_clicks_errors()
    else:
        print("Good bye!")


if __name__ == '__main__':
    main()
