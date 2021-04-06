# Terraform

## Requirements

- Terraform 0.12.24

## Preliminary step
Before inizialing the infrastructure, there is a preliminary step whose aim is to create the S3 bucket
that will contain the ``terraform states``. 

In the project root you'll find the ``init.sh`` script, that will create on S3 the bucket `empatica-tf-states`.

To run it, type:
```
./init.sh
```

## Terraform inizialization
The first thing to do before deploying the architecture, is to initialize a working directory containing Terraform 
configuration files. 

This command performs several different initialization steps in order to prepare the current working directory for 
use with Terraform:
- backend installation
- child module installation
- plugin installation

To init our specific infrastructure, navigate inside the infra folder `fd2s/infra`, and type:
```
terraform init
```

The command should create a `.terraform` folder inside the `fd2s/infra`. 

## Plan
Before applying, if you want to get an idea about the resources that will be created, just type:
```
terraform plan
```

## Apply
Once the backend has been inizialiazed, you are free to deploy the tf infrastructure: 
```
terraform apply
```

You'll be asked to confirm the planned infrastructure. 
If you want to auto approve the plan, use: 
```
terraform apply --auto-approve
```

This command will deploy the overall solution presented in the root README.md, and it will deploy: 
1) S3 buckets
    1) ``empatica-artifactory``: bucket intended to contain the lambda deployment packages
    2) ``empatica-model-x``: bucket intended to contain the daily data coming from each device
2) Cloudwatch rule 
    1) ``trigger-model-x-anomaly-detection``: crontab rule that triggers the overall detection system
3) Lambda
    1) ``empatica-AnomalyOrchestration``: lambda that is triggered by the above mentioned cloudwatch
    rule, gets the list of devices to check and sends a message to the SQS with the details about the devices to check
    2) ``empatica-TemperatureDetection``: lambda triggered by the SQS code, and it is responsible of performing the
    anomaly detection on the temperature signal.
    2) ``empatica-PPGDetection``: lambda triggered by the SQS code, and it is responsible of performing the
    anomaly detection on the PPG signal
4) SQS
    1) ``sqs-model-x-ppg``: code for device PPG details sharing
    2) ``sqs-model-x-temp``: code for device Temperature details sharing  

## Destroy

Once you want to destroy the infrastructure, it is sufficient to launch the command:
```
terraform destroy
```