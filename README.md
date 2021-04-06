# FD2S (Faulty Devices Detection System)

## Data understanding

Before lowering my head and writing even one single line of code, an essential step is to understand the data I'm working with.
Developing a fault detection system without knowking the nature of data could be quite challenging.

Each device is sending across 3 kinds of signals:

- A photoplethysmogram (PPG) signal
- A wrist temperature signal
- A detection of on-wrist signal

| Signal name | Description                                                                        | Frequency - Period         | Note                           |
| ----------- | ---------------------------------------------------------------------------------- | -------------------------- | ------------------------------ |
| PPG         | Signal about variations of blood volume changes in the microvascular bed of tissue | 64Hz - 1 sample per 0.016s |                                |
| Wrist Temp  | Temperature detected on the wrist in cents of °C                                   | 4Hz - 1 sample per 0.25s   |                                |
| On-wrist    | Detection whether the devices is worn or not                                       | 1Hz - 1 sample per second  | This values are always correct |

## EDA

docker run -it -v /Users/alessandro.negrini/Personal/fd2s/:/home/jovyan/work --rm -p 8888:8888 jupyter/pyspark-notebook

## Solution Architecture

![Architecture](./resources/architecture.png "Solution Architecture")

This is the cloud architecture I have thought to be one of the best one, given both the problem requests and the
 problem constraints. 

**Note: the services used are 100% usable in an AWS free tier account.**  
  
On the left side of the architecture diagram you can see three buckets:
 - **empatica-tf-states**: it is the bucket that is solely used by the terraform backend to store the terraform states. 
 - **empatica-artifactory**: it is the bucket intended to contain the lambda deployment packages
 - **empatica-model-x**: it is the bucket intended to host the data coming from the devices, organized as per data and
 per device id (*ass1)

All the buckets do not allow any public access. 

The overall computation is triggered by a `cloudwatch crontab rule`:
- **trigger-model-x-anomaly-detection**: it is a rule that at 01:00 of a given day, triggers the 
`empatica-AnomalyOrchestration`. 
The reason why I decided to use a Cloudwatch crontab rule and not a rule based on the PutItem on S3, is because I didn't 
the way data were uploaded (single file vs batch files) (*ass2)

The just mentioned Cloudwatch rule, in turn, triggers a lambda called ``empatica-AnomalyOrchestration``, that, as the
name suggests, is responsible of orchestrating the real failure detection logic.
Rather than being a real orchestrator, this lambda performs different steps: 
1) it gets the current day from the event received in input:
    ```
   {
       ...
       time:'2021-02-05T01:00:00'
       ...
   }
   ```
2) it evaluates the previos day date, in the format of ``YYYY/MM/DD``. In this case `2021/02/04`
3) it lists all the objects in the ``empatica-model-x`` bucket having the ``2021/02/04`` as a path substring.
For example: 
```
empatica-model-x/2021/02/04/device_001/ppg_green.csv
empatica-model-x/2021/02/04/device_002/ppg_green.csv
empatica-model-x/2021/02/04/device_001/temperature.csv
empatica-model-x/2021/02/04/device_002/temperature.csv
empatica-model-x/2021/02/04/device_001/on_wrist.csv
empatica-model-x/2021/02/04/device_002/on_wrist.csv
```
It then extracts the ``device-id`` from the path:
```
device_001
device_002
```
4) for each device extracted, an object is created, in the form of: 
```
{
    day: '2021/02/04'
    device: 'device_001'
}
```
5) each object is then sent to two SQS queues:
- ``sqs-model-x-ppg``
- ``sqs-model-x-temp``

SQS queues have been introduced in the architecture for triggering the lambdas containing the failure detection logic 
in an **asyncronous** way. 
Both of the two queues have a Lambda trigger in place, and each event triggers the failure detection logic lambda: 
- each event on ``sqs-model-x-ppg`` triggers the ``empatica-PPGDetection`` lambda
- each event on ``sqs-model-x-temp`` triggers the ``empatica-TempDetection`` lambda



#### Assumptions
- ass1: 
the structure on which data is saved (YYYY/MM/DD/< deviceid >/< filename >.csv) gives me an hint about the way data is updated. 
The fact that there is one single file per device per day, suggests me that the ingestion is not done using a streaming
system, but rather in a batch mode (daily frequency). 
Thus, I will assume that every day, somewhat (or someone) copies data inside the ``empatica-model-x`` with the following
structure: 
  * `YYYY/MM/DD/<deviceid>/ppg_green.csv`
  * `YYYY/MM/DD/<deviceid>/temperature.csv`
  * `YYYY/MM/DD/<deviceid>/on_wrist.csv`
    
- ass2: 
I assume that by 01:00:00 every device data regarding the previous day has been uploaded. I decided to not trigger the 
rule at 00:00 to leave a contingency for those data whose started to be uploaded slightly before midnight. 


### Solution frequency computation

### How does the solution scale?

### Solution limits 

