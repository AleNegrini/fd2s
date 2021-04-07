# Lambda
As shown in the general architecture the solution is made up of three functions:
- _empatica-AnomalyOrchestration_
- _empatica-TempDetection_
- _empatica-PPGDetection_ 

Each lambda has its own folder, but the structure is the same for all of them. 
As well as the instructions on how to build and upload the deployment package.

## Useful scripts
- `run-build.sh`: it creates the lambda deployment package, that is a zip containing the lambda code and its 
dependencies. This script must be launched before applying the whole infrastructure
- `run-upload.sh`: it uploads the lambda deployment package to the S3 bucket. It is used only when you change the code and you need
to re-deploy the Deployment package to AWS. 
- `run-clean.sh`: it deleted old versions of packages and deployment packages
- `prepare-job.sh`: it runs in order the scripts `run-clean.sh`, `run-build.sh` and `run-upload.sh`

## Run lambda 
If you'd like to manually test them, each lambda has its own input parameter:

### empatica-AnomalyOrchestration
Sample input

The cloudwatch rule sends a quite big event, but if you need to simulate the lambda as it were running a time T, you
can use this simple input.
Supposing you are simulating the lambda run at time T = '2021-02-05T01:00:00'
```
{
    "time": "2021-02-05T01:00:00"
}
```
I remind that the orchestration lambda running at time T will check all the devices at time T-1

### empatica-TempDetection
In an always-running solution the lambda is triggered by SQS events. 
As well as for the Cloudwatch events, the SQS will trigger the lambda including the message sent over the queue, plus 
other framing data.

If you want to manually trigger this lambda for checking a device D at day T, it's enough to pass this parameter: 
 ```
{
    "Records": 
        [
            {"body": "{\"day\":\"2021/02/02\", \"device\":\"device_001\"}"}
        ]
}
```

### empatica-PPGDetection
The same considerations for the ``empatica-TempDetection`` applies for this Lambda