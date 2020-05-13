import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

# Creating sqs client
sqs = boto3.client('sqs')

def create_queue(name, attributes=None):
    """
    Creates an Amazon SQS queue.

    Usage is shown in usage_demo at the end of this module.

    :param name: The name of the queue. This is part of the URL assigned to the queue.
    :param attributes: The attributes of the queue, such as maximum message size or
                       whether it's a FIFO queue.
    :return: A Queue object that contains metadata about the queue and that can be used
             to perform queue operations like sending and receiving messages.
    """
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

    # Creating test_devops_makelaars queue
    makelaars_queue = create_queue(
        prefix + 'makelaars',
        {
            'MaximumMessageSize': str(1024),
            'ReceiveMessageWaitTimeSeconds': str(20)
        }
    )
    response = sqs.get_queue_url(QueueName=prefix + 'makelaars')
    print("Created the queue with URL:", response['QueueUrl'])

    # Creating test_devops_makelaars_errors queue
    makelaars_errors_queue = create_queue(
        prefix + 'makelaars_errors',
        {
            'MaximumMessageSize': str(4096),
            'ReceiveMessageWaitTimeSeconds': str(10),
            'VisibilityTimeout': str(300),
        }
    )
    response = sqs.get_queue_url(QueueName=prefix + 'makelaars_errors')
    print("Created the queue with URL:", response['QueueUrl'])

    # test_devops_new_houses
    new_houses_queue = create_queue(prefix + 'new_houses')
    response = sqs.get_queue_url(QueueName=prefix + 'new_houses')
    print("Created the queue with URL:", response['QueueUrl'])

    # Creating test_devops_new_houses_errors queue
    new_houses_errors_queue = create_queue(prefix + 'new_houses_errors')
    response = sqs.get_queue_url(QueueName=prefix + 'new_houses_errors')
    print("Created the queue with URL:", response['QueueUrl'])
creating_queues()