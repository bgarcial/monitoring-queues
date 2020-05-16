#!/bin/bash
echo "Notification error message to the queue ..."
for i in {1..5}
do
   echo "Sending $i error object entry"
   #aws sqs send-message-batch --queue-url https://sqs.eu-west-1.amazonaws.com/138290733079/test_devops_makelaars	--entries file://send-houses-batch.json  > ./test.output
   aws sqs send-message-batch --queue-url $1 --entries file://$2  > ./test.output
done
echo "... messages sent to: $1"
cat ./test.output