variable "time" {
  default = "00 23"
}

locals {
  schedule_expression = "cron(${var.time} * * ? *)"
}

resource "aws_cloudwatch_event_rule" "trigger-model-x-anomaly-detection" {
  name                = "trigger-model-x-anomaly-detection"
  description         = "Trigger the anomaly detection"
  schedule_expression = local.schedule_expression
}

resource "aws_cloudwatch_event_target" "check_foo_every_five_minutes" {
  rule      = "${aws_cloudwatch_event_rule.trigger-model-x-anomaly-detection.name}"
  target_id = "${var.prefix}-TriggerAnomalyDetection"
  arn       = "${aws_lambda_function.anomaly_orchestration_lambda.arn}"
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_lambda" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = "${var.prefix}-AnomalyOrchestration"
  principal     = "events.amazonaws.com"
  source_arn    = "${aws_cloudwatch_event_rule.trigger-model-x-anomaly-detection.arn}"
}
