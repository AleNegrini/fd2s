resource "aws_iam_role" "temp-detection-role" {
  name = "${var.prefix}-temp-detection-role"
  path = "/"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF


  tags = {
    project = var.prj_code
    dept    = var.data_dept
    env     = var.env
  }
}

resource "aws_iam_policy" "temp-detection-policy" {
  name        = "${var.prefix}-temp-detection-policy"
  description = "Policy allowing to do temperature anomaly detection"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "ec2:CreateNetworkInterface",
                "ec2:DescribeNetworkInterfaces",
                "ec2:DeleteNetworkInterface"
            ],
            "Resource": "*"
        },
        {
          "Action": "dynamodb:PutItem",
          "Effect": "Allow",
          "Resource": [
            "${aws_dynamodb_table.temp_fd2s_history.arn}",
            "${aws_dynamodb_table.ppg_fd2s_history.arn}"
          ]
        },
        {
          "Effect": "Allow",
          "Action": ["s3:ListBucket"],
          "Resource": ["${aws_s3_bucket.empatica-signals-model-X.arn}"]
        },
        {
          "Effect": "Allow",
          "Action": [
            "s3:GetObject"
          ],
          "Resource": ["${aws_s3_bucket.empatica-signals-model-X.arn}/*"]
        },
        {
          "Action": "sqs:*",
          "Effect": "Allow",
          "Resource": [
            "${aws_sqs_queue.empatica-queue-ppg.arn}",
            "${aws_sqs_queue.empatica-queue-temp.arn}"
          ]
        }
    ]
}
EOF


}

resource "aws_iam_role_policy_attachment" "attach-role-policy" {
  role       = aws_iam_role.temp-detection-role.name
  policy_arn = aws_iam_policy.temp-detection-policy.arn
}

resource "aws_lambda_function" "temp_lambda" {
  s3_bucket     = "empatica-artifactory"
  s3_key        = "temp_failure_detection_dp.zip"
  function_name = "${var.prefix}-TemperatureDetection"
  role          = aws_iam_role.temp-detection-role.arn
  handler       = "lambda_function.lambda_handler"
  timeout       = 300
  memory_size   = 1024

  layers = ["arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-python38-pandas:30"]

  runtime = "python3.8"

  environment {
    variables = {
      WINDOW           = "1200"
      LOWER_TEMP       = "3200"
      UPPER_TEMP       = "4300"
      VOLATILITY_LIMIT = "50"
    }
  }

  tags = {
    project = var.prj_code
    dept    = var.data_dept
    env     = var.env
  }
}

resource "aws_lambda_function" "ppg_lambda" {
  s3_bucket     = "empatica-artifactory"
  s3_key        = "ppg_failure_detection_dp.zip"
  function_name = "${var.prefix}-PPGDetection"
  role          = aws_iam_role.temp-detection-role.arn
  handler       = "lambda_function.lambda_handler"
  timeout       = 300
  memory_size   = 1024

  layers = ["arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-python38-pandas:30"]

  runtime = "python3.8"

  environment {
    variables = {
      MAX_PPG_INF = "15000"
      MAX_PPG_SUP = "21000"
      MIN_PPG_INF = "3000"
      MIN_PPG_SUP = "6000"
      AVG_PPG_INF = "5000"
      AVG_PPG_SUP = "11000"
    }
  }

  tags = {
    project = var.prj_code
    dept    = var.data_dept
    env     = var.env
  }
}

resource "aws_iam_role" "anomaly_orchestration_role" {
  name = "${var.prefix}-anomaly-orchestration-role"
  path = "/"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF


  tags = {
    project = var.prj_code
    dept    = var.data_dept
    env     = var.env
  }
}

resource "aws_iam_policy" "anomaly-orchestration-policy" {
  name        = "${var.prefix}-anomaly-orchestration-policy"
  description = "Policy allowing to run orchestrator lambda"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "ec2:CreateNetworkInterface",
                "ec2:DescribeNetworkInterfaces",
                "ec2:DeleteNetworkInterface"
            ],
            "Resource": "*"
        },
        {
          "Effect": "Allow",
          "Action": ["s3:ListBucket"],
          "Resource": ["${aws_s3_bucket.empatica-signals-model-X.arn}"]
        },
        {
          "Effect": "Allow",
          "Action": [
            "s3:GetObject"
          ],
          "Resource": ["${aws_s3_bucket.empatica-signals-model-X.arn}/*"]
        },
        {
          "Action": "sqs:*",
          "Effect": "Allow",
          "Resource": [
            "${aws_sqs_queue.empatica-queue-ppg.arn}",
            "${aws_sqs_queue.empatica-queue-temp.arn}"
          ]
        }
    ]
}
EOF


}

resource "aws_iam_role_policy_attachment" "attach-role-policy_orch" {
  role       = aws_iam_role.anomaly_orchestration_role.name
  policy_arn = aws_iam_policy.anomaly-orchestration-policy.arn
}

resource "aws_lambda_function" "anomaly_orchestration_lambda" {
  s3_bucket     = "empatica-artifactory"
  s3_key        = "anomaly_orchestration_dp.zip"
  function_name = "${var.prefix}-AnomalyOrchestration"
  role          = aws_iam_role.anomaly_orchestration_role.arn
  handler       = "lambda_function.lambda_handler"
  timeout       = 120
  memory_size   = 128

  runtime = "python3.8"

  environment {
    variables = {
      TEMP_SQS_URL = "${aws_sqs_queue.empatica-queue-temp.id}"
      PPG_SQS_URL  = "${aws_sqs_queue.empatica-queue-ppg.id}"
      BUCKET_NAME  = "${aws_s3_bucket.empatica-signals-model-X.id}"
    }
  }

  tags = {
    project = var.prj_code
    dept    = var.data_dept
    env     = var.env
  }
}
