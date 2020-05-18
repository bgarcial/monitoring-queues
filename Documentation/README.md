# Documentation

## Use case

Team 1 queues:
- test_devops_makelaars
- test_devops_makelaars_errors

Team 2 queues:
- test_devops_new_houses
- test_devops_new_houses_errors
- test_devops_edited_houses
- test_devops_edited_houses_errors
- test_devops_removed_houses
- test_devops_removed_houses_errors

Team 3 queues:
- test_devops_stats_phone_clicks
- test_devops_stats_phone_clicks_errors
- test_devops_stats_facebook_clicks
- test_devops_stats_facebook_clicks_errors

---
## Requirements for monitoring
1. All teams want to be notified if there are any errors in the error SQS (_error queues).
2. Team 1 and Team 2 want to be notified if there are more than 10 messages in `test_devops_new_houses` and `test_devops_makelaars queues`.
3. Team 3 wants to be notified if there are more than 25 messages in standard non-error
queues.
---

## 1. Problem identified
The number of queues is growing every month

## 2. Assumptions and Deployment Architecture decisions made

According to the teams requirements, the focus of the problem/opportunity is metrics collection and monitoring of the queues. The following workflow shows an SQS system on Amazon Cloud, receiving batch messages from an external application.
Some assumptions are presented here:

### 2.1  SCOPE OF THE SOLUTION
- The focus of the collection and monitoring will be the `ApproximateNumberOfMessagesVisible` aws metric in all the queues defined.
    - This metric is being referenced in the [metrics YAML definition file](https://github.com/bgarcial/monitoring-queues/blob/master/cloudwatch/metrics/example.yml#L20).

    **IMPORTANT TO KEEP IN MIND IN THE SOLUTION**

    - There are another  SQS metrics referenced in the [metrics YAML definition file](https://github.com/bgarcial/monitoring-queues/blob/master/cloudwatch/metrics/example.yml#L20)  but these are not being collected or monitored since our approach solution is only receiving messages in the queues mentioned [from an external script](https://github.com/bgarcial/monitoring-queues/blob/master/queue-workflow.py), therefore either processors or consumers entities for the queue's messages were not involved here in this solution.

    - I also referenced in that file other metrics associated to other AWS services. These ones and the other SQS (different to `ApproximateNumberOfMessagesVisible`) are not being analysed here in this case. I just put them there just to be aware about the monitoring possibilities from Prometheus and Grafana towards different cloud resources in order to keep them in mind for the future.

### 2.2. TOOLS/LANGUAGES USED IN THE SOLUTION

Since we need to collect the `ApproximateNumberOfMessagesVisible` queue's metric and visualize them and send notifications according to the thresholds (defined at the requirement section) we will use the following tools for the process:

1. **YAML File definition queues**: The names of the queues were defined [here](https://github.com/bgarcial/monitoring-queues/blob/master/queues_definition-2.yml).

2.  **AWS python SDK** to create and send messages to the queues.
    - A [python script](https://github.com/bgarcial/monitoring-queues/blob/master/queue-workflow.py) read the YAML definition file, create and send messages to the defined queues

3.  **[Prometheus](https://prometheus.io/)** is being used for collecting data metrics (as mentioned and I will show in the diagram above) from AWS/SQS as a monitoring target by scrapping its http endpoint exposed by [cloudwatcher exporter](https://github.com/prometheus/cloudwatch_exporter), so in this way I managed to collect the SQS cloud watch metrics from Amazon and focus on the `ApproximateNumberOfMessagesVisible` metric.
    ```
    ubuntu@ip-172-31-27-129:/etc/prometheus$ cat prometheus.yml
    global:
    scrape_interval: 15s
    scrape_configs:
    - job_name: 'prometheus'
        scrape_interval: 5s
        static_configs:
        - targets: ['localhost:9090']
    - job_name: 'node_exporter'
        scrape_interval: 5s
        static_configs:
        - targets: ['localhost:9100']
    - job_name: cloudwatch
        scrape_interval: 5s
        honor_labels: true
        static_configs:
        - targets: ['localhost:9106']
    ubuntu@ip-172-31-27-129:/etc/prometheus$
    ```

4. **[Grafana](https://grafana.com/docs/grafana/latest/)** is being used as a visualization, alerting and monitoring tool by importing inside it the [AWS/SQS dashboard](https://grafana.com/grafana/dashboards/584) and [Prometheus datasource](https://prometheus.io/docs/visualization/grafana/) which consume the prometheus scrapper running in the [:9090](http://monitoring.bgarcial.me:9090/) port

    - I want to point out here, that Prometheus datasource is not necessary to be imported inside grafana, since we already getting the metrics from cloudwatcher exporter (from prometheus) and consuming it from AWS/SQS dashboard in grafana.
    > Since Prometheus exports important data about itself, as an HTTP endpoint it can scrape and monitor its own health. controls what resources Prometheus monitors.

    - So in that way, could be interesting to visualize some prometheus metrics such as we can see [here in its datasource form grafana](http://monitoring.bgarcial.me:3000/d/T1n2T5RGk/prometheus-2-0-stats?orgId=1&refresh=1m)
        - In some emails I sent you the access to grafana :)
        - The most interesting for this case is the scrape duration, talking about the different points in the time where the cloudwatcher and other exporters were scrapping data from external sources, in this case from AWS/SQS api.

          This is a chart from the last 24 hours activity related to the cloudwatch exporter. It was when grafana detect data for the queues and metric defined. (I will talk about queues, metric and alerts later on.)


          ![Prometheus exporter](https://cldup.com/BLfaClXIcN.png "Prometheus exporter")
          Even we can create queries and alarms by using prometheus metrics inside it, according to the scrapper jobs defined in its configuration.

          ![Prometheus exporter](https://cldup.com/PbXWMWzTgB.png "Prometheus exporter")

    As I mentioned, from grafana I am not only visualizing, also I am creating alerts rules from `ApproximateNumberOfMessagesVisible` AWS/SQS metric in every queue defined and sending notifications to Slack channels by creating grafana notification channels connecting to slack via [incoming webhooks](https://api.slack.com/messaging/webhooks)

5. **Slack as a notification reception system**:

Many teams around the world use Slack as a collaboration and messaging tool, so it is suited to let them know to the teams (teams 1,2 and 3 defined in the problem) if something happen with the queues.

I created a workspace called `https://sofi-testing.slack.com/` associated to my personal Gmail account.
There the `#team-1`, `#team-2` and `#team-3` channels were created.

![Slack channels ](https://cldup.com/sRdxyXarxG.png "Prometheus exporter")

---
So according to all previously described, this is the workflow that I implemented in this solution, located in the
eu-west-1 Europe (Ireland) region.


![SQS Architecture approach](https://cldup.com/8SEXKmqXVR.jpg "SQS Architecture approach")




