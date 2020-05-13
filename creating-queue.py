import boto3
sqs = boto3.client('sqs')

def creating_queue(queue_name):
    response = sqs.create_queue(
        QueueName=queue_name,
            Attributes = {
                'DelaySeconds': '60',
                'MessageRetentionPeriod': '86400'
            }
        )
    print (response['QueueUrl'])

def getting_queues():
    response = sqs.list_queues()
    print(response['QueueUrls'])

def sending_message(queue_url):
    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl = queue_url,
        DelaySeconds=10,
        MessageAttributes={
            'Title': {
                'DataType': 'String',
                'StringValue': 'The Whistler'
            },
            'Author': {
                'DataType': 'String',
                'StringValue': 'John Grisham'
            },
            'WeeksOn': {
                'DataType': 'Number',
                'StringValue': '6'
            }
        },
        MessageBody=(
            'Information about current NY Times fiction bestseller for '
            'week of 12/11/2016.'
        )
    )

    print(response['MessageId'])

#creating_queue('SQS_CREATING_PROPERTIES')
#getting_queues()
queue_url='https://eu-west-1.queue.amazonaws.com/138290733079/SQS_CREATING_PROPERTIES'
sending_message(queue_url)