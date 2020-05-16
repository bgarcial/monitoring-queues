aws sqs send-message --queue-url https://sqs.eu-west-1.amazonaws.com/138290733079/test_devops_makelaars --message-body "Information about the largest city in Any Region." --delay-seconds 10 --message-attributes file://send-message.json

aws sqs send-message-batch --queue-url https://sqs.eu-west-1.amazonaws.com/138290733079/test_devops_new_houses --entries file://send-message-batch.json