# Collecting metrics from Amazon AWS/SQS queues and monitoring

## Problem:

There are some SQS queues on amazon (+/- 10 queues, but the number of queues is growing
every month). Queues are for different applications, different teams, and have different
characteristics (error queues, different purposes, different thresholds etc.).

The teams are responsible for adding new queues and specifying which queues are applicable to be
monitored.

## Target

As a DevOps team we would like to monitor these queues by providing an automation solution
which creates a monitor per queue according to a definition file where the queues are
specified. So that we can be alerted whenever something goes wrong with the queues.

---

# Architecture approach defined.

![SQS Architecture approach](https://cldup.com/x3Lkb9b9Us.jpg "SQS Architecture approach")

You can find what is this solution about at the [Documentation section](https://github.com/bgarcial/monitoring-queues/tree/master/Documentation)

