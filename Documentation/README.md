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


![SQS Architecture approach](https://cldup.com/DvYWe9gPRs.jpg "SQS Architecture approach")

---

## 3. Some important things I assume are already created

As a starting point, in order to make effective the checking of this solution, I will assume that the following activities
already were created/deployed in order to anybody who wants to come across of the solution, can focus on the collection metrics, monitoring and alerting activities since those activities are the essentials of this approach.

1. Amazon EC2 instance is already created.
    + A security group should be associated to it, in order to expose the following services/ports
        + SSH
        + 3300 to be used by grafana
        + 80 standard http traffic since prometheus is exposed by nginx
        + 9090 for prometheus metrics (it is not necessary)
        + 9106 to be used by cloudwatcher prometheus scrapper
        + 9100 is used by the `node_exporter` prometheus scrapper
            + It brings host level metrics (cpu, disk, system load, network traffic, etc) about machine where prometheus is. (It is not necessary)
            + You can check the endpoint [here](http://monitoring.bgarcial.me:9100/metrics)
            + Do you remember Prometheus datasource was imported on grafana right? so [you can check node exporter metrics here in grafana dashboard](http://monitoring.bgarcial.me:3000/d/ZpqaY0JWk/node-exporter-for-prometheus-dashboard-english-compatibility-version)
2. Prometheus was installed on EC2 instance
    + [cloudwatcher](https://github.com/prometheus/cloudwatch_exporter) scrapper was configured on `/etc/prometheus/prometheus.yml`
        + [cloudwatcher http endpoint is running](https://github.com/prometheus/cloudwatch_exporter#building-and-running) by using `9106` port. You can check the metrics scrapped here in the endpoint http://monitoring.bgarcial.me:9106/metrics which perform requests AWS/SQS cloudwatch metrics
            + To do that, `aws cli` and `aws credentials` [should be configured](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) inside the ec2 instance where cloudwatcher will be running in order to contact the SQS metrics to be scrapped.
            The result should be something like this:

            ![aws credentials](https://cldup.com/2Zkt9xqlHz.png "aws credentials")
    + Installed nginx and adding basic HTTP authentication to prometheus.
3. Grafana service application was installed on EC2 Instance
    + [AWS/SQS dashboard](https://grafana.com/grafana/dashboards/584) was imported in grafana
    + [Prometheus datasource](https://prometheus.io/docs/visualization/grafana/) was imported on grafana
    + Error queues and standard queues dashboard and alert rules and notification channels should be created in grafana.
        + Since these actions constitute the focus of the solution will get into them later on in at **#4 separate section.**
4. Slack workspace [should be created](https://slack.com/intl/en-nl/help/articles/206845317-Create-a-Slack-workspace).
    + `#team-1`, `#team-2` and `#team-3` channels should be created inside workspace.
    + Slack incoming webhooks [should be created](https://api.slack.com/messaging/webhooks) to post messages to `#team-1`, `#team-2` and `#team-3` channels
        + These webhooks will be used by the notification channels created in grafana in order to post messages to a specific channel team.
        + In my case I decided to create a webhook per error and standard queue queue
            + This is not necessarily mandatory, I was checking from slack perspective why sometimes I experiencing some delay in the notifications
            when grafana send the alert to slack. Later on during the process I will realise that also something important to evaluate here is [the way like grafana alerts works](https://grafana.com/docs/grafana/latest/alerting/create-alerts/#alert-rule-fields). I will reference that later on in at **#4 separate section.**

            + Is good to point out that for instance all the error queues could use only one incoming webhook to post to `#team-1` channel and the same for the other channels, but I decided use a webhook per queue. Despite behind this kind of decisions could do exist non-functional requirementes or business decisions, do it or don't is a free decision.

        ![slack incoming webhooks](https://cldup.com/mEvHwQm0zE.png "slack incoming webhooks")


---

## 4. About Alerts, notification channels and error and standard queues dashboard in Grafana

If someone wants to check the behavior of the solution, there are some important facts to keep in mind about how grafana
is reading the metrics and sending alerts notification when defined thresholds are exceeded.

Since one of the general requirements of the problem says:
>A monitor per queue needs to be created

Therefore, I created a panel dashboard for error queues and standard non-errors queues.

### 4.1. Error queues panel dashboards:

According to the definition problem, there are the following error queues:
- `test_devops_makelaars_errors`: #team-1
- `test_devops_new_houses_errors`: #team-2
- `test_devops_edited_houses_errors`: #team-2
- `test_devops_removed_houses_errors`: #team-2
- `test_devops_stats_phone_clicks_errors`: #team-3
- `test_devops_stats_facebook_clicks_errors`: #team-3

I created the **Error queues** dashboard for those queues (It has starred to be found easily and also has the `Use me` tag)

![test_devops_makelaars_errors dashboard](https://cldup.com/AxcMOySdzQ.png "test_devops_makelaars_errors dashboard")

Let's walk through of the `test_devops_makelaars_errors` dashboard  error queue creation

#### 4.1.2 Query section

When you create a dashboard and you can defined queries to be performed from it.
In this case I can select the Cloudwatch target because I imported  the AWS/SQS Cloudwatch  dashboard which allow me to
see the metrics that cloudwatch_exporter collect from prometheus instance. Let's point out other parameters such as:

- **Region**, the `eu-west-1` required.
- **Namespace**. I have plenty of AWS namespace resources according to the scrapped ones defined [in the metrics yaml file](https://github.com/bgarcial/monitoring-queues/blob/master/cloudwatch/metrics/example.yml#L20) used by cloudwatch_exporter from prometheus.

  Every namespace resource defined there will appear in this dropdown selection control. The `AWS/SQS` namespace is the selected here.
- **Metric Name**: Remember the focus here is the `ApproximateNumberOfMessagesVisible`
- **Stats**: `sum()`
  Since the condition to be evaluated in the error queues is:
  >All teams want to be notified if there are any errors in the error SQS (_error queues).

  I decided to select `sum()` in order to get the total count of the messages which are visible on the queue and when that value exceed the
  threshold defined (**number of messages visible above 0** - I will describe this condition later on), then trigger the notification to `#team-1`, `#team-2` and `#team-3` slack channels

- **Dimension**. `QueueName` is the dimension selected.
    - It has direct relation with the defined on the [examples.yaml](https://github.com/bgarcial/monitoring-queues/blob/master/cloudwatch/metrics/example.yml#L21) file.
    - According to the [documentation](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-available-cloudwatch-metrics.html):

      >The only dimension that Amazon SQS sends to CloudWatch is QueueName. This means that all available statistics are filtered by QueueName.


![test_devops_makelaars_errors dashboard](https://cldup.com/GRgjmTORHm.png "test_devops_makelaars_errors dashboard")

#### 4.1.3. Visualization section

There are plenty of options to play around visualizations

![test_devops_makelaars_errors dashboard](https://cldup.com/-1TzuhWPsO.png "test_devops_makelaars_errors dashboard")

#### 4.1.4. General options
Here is possible to name the dashboard, in this case `test_devops_makelaars_errors`

![test_devops_makelaars_errors dashboard](https://cldup.com/Vq3lu_rUsm.png "test_devops_makelaars_errors dashboard")

#### 4.1.5. Alert options
Here the alert rule for the queue will be created. An alert has some important sections.

- **Rule**: Here the rule is created
    - **Evaluate every**: According to the [documentation](https://grafana.com/docs/grafana/latest/alerting/create-alerts/#alert-rule-fields) ...
      >Specify how often the scheduler should evaluate the alert rule. This is referred to as the evaluation interval.
    + **For**:
      >Specify how long the query needs to violate the configured thresholds before the alert notification triggers.

      Basically I am saying to grafana that check this rule every 1m during 1 minute.
      If during this period the condition(s) immediately below referenced will be checked and if the threshold is exceed, the alert will be triggered.

- **Conditions**: [The only parameter could be specified here](https://grafana.com/docs/grafana/latest/alerting/create-alerts/#conditions) is a condition based on  query defined at the **4.1.2 Query section**

    I am telling to the rule, that the query A defined, should be executed for a time range from 1m ago to now
and if the messages are above `0` the alerting will be triggered.

    I am defining in the condition `IS ABOVE 0` since all teams want to be notified if there any errors in the error SQS. This means at least if 1 message arrive to those queues.


![test_devops_makelaars_errors dashboard](https://cldup.com/IgJhD1Nqzl.png "test_devops_makelaars_errors dashboard")

- **No data and error handling section**
I am telling to the rule, keep the alert when there are errors on the queue or data are not found.
Normally due to the queue nature, always should there were data in them (?)

- **Notifications section**
    - **Send to**: Will be necessary to create first notification channels in order to have them available and select them here
    As we can see the `msg_makelaars_errors-to-team1`, `msg_makelaars_errors-to-team2` and `msg_makelaars_errors-to-team3` slack notification channels were used here. What does it means?
    Since `#team-1`, `#team-2` and `#team-3` channels should be notified when a message is visible on the queue  errors, and since one slack notification channel only can POST messages to one slack channel, then three slack notifications channels were created on grafana on this way:

    The `msg_makelaars_errors-to-team1` notification channel post messages to `#team-1` slack channel by making use of one of the incoming webhooks created previously at the [**3. Some important things I assume already created**](https://github.com/bgarcial/monitoring-queues/tree/master/Documentation#3-some-important-things-i-assume-are-already-created) section

    ![test_devops_makelaars_errors channel](https://cldup.com/NkC0YapYAK.png "test_devops_makelaars_errors channel")

    The incoming url webhook selected here only post messages to `#team-1` slack channel.

    So in the same way, the `msg_makelaars_errors-to-team2` notification channel post messages to `#team-2`

    ![test_devops_makelaars_errors channel](https://cldup.com/PJMgp-LQG6.png "test_devops_makelaars_errors channel")

    And the same case for the `msg_makelaars_errors-to-team3` notification channel. Its only will post messages to `#team-3` slack channel

    ![test_devops_makelaars_errors channel](https://cldup.com/paOi1EKWYQ.png "test_devops_makelaars_errors channel")

    The Username field is the username assigned to the slack application created which is interacting with the channels to send the messages.
    The string at the Mention users field is the user id of the user I want to notify when the alert is triggered.

    Once these notification channels are created, those can be selected at the **Send To** section, and I can also customize the alert message.


    ![test_devops_makelaars_errors channel](https://cldup.com/OPpcfR3WqG.png "test_devops_makelaars_errors channel")

So once the alert rule is created you will see that alert rule will be referenced here:

![alert rules](https://cldup.com/aJi5FkPd_D.png "alert rules")

Is necessary do the same previous steps for the other `_error_queues` since all teams should receive notification when at least 1 message arrive to those queues.


**NOTE**:

You can see there other alert rules for the other error and standard non-error queues defined because their dashboards and alerts and notification channels already were created and those queues already have messages exceeding the thresholds defined (in the error queues case above 0 messages) and in the standard non-errors queues above 25 messages

(I will reference the non-standard dashboard and the way of send messages to the queues from pythos script later on )

---

### 4.2. Standard non-error queues panel dashboards:

According to the definition problem, there are the following Standard non-error queues:

- `test_devops_makelaars`: #team-1
- `test_devops_new_houses`: #team-2
- `test_devops_edited_houses`: #team-2
- `test_devops_removed_houses`: #team-2
- `test_devops_stats_phone_clicks`: #team-3
- `test_devops_stats_facebook_clicks`: #team-3

I created the **Standard non-error queues** dashboard for those queues (It has starred to be found easily and also has the `Use me` tag)

![dashboard](https://cldup.com/WhQo1We5_6.png "dashboard")

Let's walk through of the `test_devops_new_houses` dashboard  queue creation

![dashboard](https://cldup.com/c3ImhNNh8k.png "dashboard")

- The query section is created in the same way as I mentioned before in the error queues dashboards.
    - The same metric, namespace and `sum()` stats

    ![dashboard](https://cldup.com/ZfJgUMSguk.png "dashboard")

- **Alerting section**

But here we have  a new alert condition rules.
The requirements of the problem say:

>Team 3 wants to be notified if there are more than 25 messages in standard non-error
queues.

So this alert will be implemented for all non-error queues, so in `test_devops_new_houses` it will be:

- Look the condition defined: `WHEN sum() OF query(A,1m,now) IS ABOVE 25`
It means that the rule will be checked when the messages are more than 25 from 1m ago up to now.

![dashboard](https://cldup.com/XuVQuS0YlN.png "dashboard")

For the other non-error queues the same rule should be (and it was) created in their own dashboards

#### 4.2.1. A new requirement threshold is defined for `test_devops_new_houses` and `test_devops_makelaars`

But there are more requirements:

>Team 1 and team 2 want to be notified if there are more than 10 messages in
`test_devops_new_houses` and `test_devops_makelaars queues`.

So since this is about a new notification message, since the destination teams are differents and the threshold defined here is for different purposes I created two panel dashboards called:
+ `test_devops_new_houses_more_than_10_msgs`
+ `test_devops_makelaars_more_than_10_msgs `


![dashboard](https://cldup.com/EW0lcXNiRF.png "dashboard")

In both we have the same alert condition rule defined but with their respective notification channels and behind of tem their respective slack incoming webhooks



![dashboard](https://cldup.com/MnK9Cv4TnV.png "dashboard")

![dashboard](https://cldup.com/sSkHp5D3jm.png "dashboard")


---

## 5. Using the solution approach

Until now, is opportune to highlight these workflow has been implemented by applying all the previous described activities.

![SQS Architecture approach](https://cldup.com/DvYWe9gPRs.jpg "SQS Architecture approach")

But ... how this workflow works?

Well, let's remember I mentioned the python script is the producer of the queues and the messages sent to them. So the workflow is the following:

- The names of the queues are defined [in the yaml file](https://github.com/bgarcial/monitoring-queues/blob/master/queues_definition-2.yml)
+ Python script take every name and create que queues.
+ From python script the user or producer process has the possibility to send messages to the queue by accepting or rejecting the queue which I want to send it messages.
- Then the messages arrive to every queue selected in the previous process.
- Then Prometheus server via cloudwatch scrapper collect some SQS metrics.
    - Rememeber, tThe focus of the collection and monitoring will be the `ApproximateNumberOfMessagesVisible` aws metric in all the queues defined.
        - It is since this approach solution is only receiving messages in the queues mentioned from an external script, therefore either processors or consumers entities for the queue's messages were not involved here in this solution, so there are not presenting other situations in order to involve other metrics here.
- Grafana import Prometheus data by applying the prometheus datasource and the AWS/SQS  dashboard
- Then Grafana visualize the `ApproximateNumberOfMessagesVisible` aws metric for every queue defined (as I described along this documentation)
- Then Grafana applies some queries according to the thresholds requirements defined in order to decide if issue notifications alerts to the respective teams.
- If notifications are triggered, then those will be sent to `#team-1`, `#team-2` and `#team-3` slack channels
- Then the respective teams will be aware about if some threshold was exceeded.

### 5.1. Executing python script queue and messages producer

- The python script interact directly with AWS SQS API by using the AWS SDK.
- By executing the script all the queues required in the problem definition will be created automatically.
    - Along that way, this script allow to the user decide to which queues wants to send messages, by getting
    the `(y/n)` input user from the keyboard. It will ask you to send messages to all the error and standard queues created in the previous step.

So, let's see this process:

#### 5.1.2. Creating python virtual environment

- You can create a python virtual env via [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) or what ever alternative you want to use.
+ Once you've created the virtual environment upgrade pip package manager. `pip install --upgrade pip`
- Clone the `monitoring_queues` [repository](https://github.com/bgarcial/monitoring-queues)
+ Place yourself at the root directory `/monitoring-queues`
- There is a `requirements.txt` [file inside the project repository](https://github.com/bgarcial/monitoring-queues/blob/master/requirements.txt). It is used to install the packages dependencies for the script.
- Please execute `pip install -r requirements.txt` so the `boto3` (python aws sdk) and `pyyaml` libraries  will be installed.

#### 5.1.3. Configure aws credentials in your workstation.

Keep in mind create a special IAM user identity and not use the AWS root account.

To do that, `aws cli` and `aws credentials` [should be configured](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).

The result should be something like this:

![aws credentials](https://cldup.com/qucCuLqQK1.png "aws credentials")

#### 5.1.4. Executing the `queue-workflow.py` script

As I mentioned this script only will create the queues and eventually send messages to them if the user decide to do it.
So it is not performing the complete workflow described in the above diagram.

---
**IMPORTANT NOTES TO HIGHLIGHT**

- Creating the monitoring and alerts from the script.

Something I wish I had the time to do is create the monitoring process created by hand in grafana, from this script.
In that sense think about check  libraries like [grafana-api](https://pypi.org/project/grafana-api/) or [the official http api reference](https://grafana.com/docs/grafana/latest/http_api/) will bring ideas to pursue that.

- The python code is not following DRY principles, since the queues creation is performed by using a function for each of the 12 queues.
This is not optimal. I would like to create probably a class and separate the creation and sending messages process in different methods so the queues and the messages could be addressed by objects instances of the class and probably passing the name of the queues as a parameters to the methods.
Just an idea, probably there are better recommendations about write better code than that.

---

So let's continue with the script execution ...

When you execute `python queue-workflow.py` you will be asked about to accept the send messages process
So far just let it create the queues without send messages to any of them:

![python script](https://cldup.com/WKanPGx5Ch.png "python script")


- So apply `(y/n)n` to every question about send messages to the error and standard queues. In this output you will see how:

```
python queue-workflow.py                                                

               By creating those queues and sending them messages
               you should use your default AWS account credentials and
               might incur charges on your account.

               Do you want to continue (y/n)?y
Starting to create all queues and send messages to them.

    # ######################################
    # Creating test_devops_makelaars queue #
    # ######################################

Name of the queue created: test_devops_makelaars
URL: https://eu-west-1.queue.amazonaws.com/138290733079/test_devops_makelaars

               Do you want to send messages to test_devops_makelaars (y/n)?n
Please continue with other queues. Good bye!

    # #############################################
    # Creating test_devops_makelaars_errors queue #
    # #############################################

Name of the queue created: test_devops_makelaars_errors
URL: https://eu-west-1.queue.amazonaws.com/138290733079/test_devops_makelaars_errors

               Do you want to send messages to test_devops_makelaars_errors (y/n)?n
Please continue with other queues. Good bye!

    # #######################################
    # Creating test_devops_new_houses queue #
    # #######################################

Name of the queue created: test_devops_new_houses
URL: https://eu-west-1.queue.amazonaws.com/138290733079/test_devops_new_houses

               Do you want to send messages to test_devops_new_houses (y/n)?n
Please continue with other queues. Good bye!

    # ##############################################
    # Creating test_devops_new_houses_errors queue #
    # ##############################################

Name of the queue created: test_devops_new_houses_errors
URL: https://eu-west-1.queue.amazonaws.com/138290733079/test_devops_new_houses_errors

               Do you want to send messages to test_devops_new_houses_errors (y/n)?n
Please continue with other queues. Good bye!

    # ##########################################
    # Creating test_devops_edited_houses queue #
    # ##########################################

Name of the queue created: test_devops_edited_houses
URL: https://eu-west-1.queue.amazonaws.com/138290733079/test_devops_edited_houses

               Do you want to send messages to test_devops_edited_houses (y/n)?n
Please continue with other queues. Good bye!

    # #################################################
    # Creating test_devops_edited_houses_errors queue #
    # #################################################

Name of the queue created: test_devops_edited_houses_errors
URL: https://eu-west-1.queue.amazonaws.com/138290733079/test_devops_edited_houses_errors

               Do you want to send messages to test_devops_edited_houses_errors (y/n)?n
Please continue with other queues. Good bye!

    # ###########################################
    # Creating test_devops_removed_houses queue #
    # ###########################################

Name of the queue created: test_devops_removed_houses
URL: https://eu-west-1.queue.amazonaws.com/138290733079/test_devops_removed_houses

               Do you want to send messages to test_devops_removed_houses (y/n)?n
Please continue with other queues. Good bye!

    # ##################################################
    # Creating test_devops_removed_houses_errors queue #
    # ##################################################

Name of the queue created: test_devops_removed_houses_errors
URL: https://eu-west-1.queue.amazonaws.com/138290733079/test_devops_removed_houses_errors

               Do you want to send messages to test_devops_removed_houses_errors (y/n)?n
Please continue with other queues. Good bye!

    # ###############################################
    # Creating test_devops_stats_phone_clicks queue #
    # ###############################################

Name of the queue created: test_devops_stats_phone_clicks
URL: https://eu-west-1.queue.amazonaws.com/138290733079/test_devops_stats_phone_clicks

               Do you want to send messages to test_devops_stats_phone_clicks (y/n)?n
Please continue with other queues. Good bye!

    # ######################################################
    # Creating test_devops_stats_phone_clicks_errors queue #
    # ######################################################

Name of the queue created: test_devops_stats_phone_clicks_errors
URL: https://eu-west-1.queue.amazonaws.com/138290733079/test_devops_stats_phone_clicks_errors

               Do you want to send messages to test_devops_stats_phone_clicks_errors (y/n)?n
Please continue with other queues. Good bye!

    # ##################################################
    # Creating test_devops_stats_facebook_clicks queue #
    # ##################################################

Name of the queue created: test_devops_stats_facebook_clicks
URL: https://eu-west-1.queue.amazonaws.com/138290733079/test_devops_stats_facebook_clicks

               Do you want to send messages to test_devops_stats_facebook_clicks (y/n)?n
Please continue with other queues. Good bye!

    # #########################################################
    # Creating test_devops_stats_facebook_clicks_errors queue #
    # #########################################################

Name of the queue created: test_devops_stats_facebook_clicks_errors
URL: https://eu-west-1.queue.amazonaws.com/138290733079/test_devops_stats_facebook_clicks_errors

               Do you want to send messages to test_devops_stats_facebook_clicks_errors (y/n)?n
We've finished. Good bye!
```