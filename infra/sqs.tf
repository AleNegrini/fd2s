locals {
  queue_ppg  = "${var.prefix}-sqs-model-x-ppg"
  queue_temp = "${var.prefix}-sqs-model-x-temp"
}

resource "aws_sqs_queue" "empatica-queue-ppg" {
  name                       = "${local.queue_ppg}"
  visibility_timeout_seconds = 500

  tags = {
    project = var.prj_code
    dept    = var.data_dept
    env     = var.env
  }
}

resource "aws_lambda_event_source_mapping" "ppg_trigger" {
  event_source_arn = aws_sqs_queue.empatica-queue-ppg.arn
  function_name    = aws_lambda_function.ppg_lambda.arn
  enabled          = true
}

resource "aws_lambda_event_source_mapping" "temp_trigger" {
  event_source_arn = aws_sqs_queue.empatica-queue-temp.arn
  function_name    = aws_lambda_function.temp_lambda.arn
  enabled          = true
}

resource "aws_sqs_queue" "empatica-queue-temp" {
  name                       = "${local.queue_temp}"
  visibility_timeout_seconds = 500

  tags = {
    project = var.prj_code
    dept    = var.data_dept
    env     = var.env
  }
}
