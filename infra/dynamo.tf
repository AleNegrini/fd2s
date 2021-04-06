locals {
  dynamo_temp = "${var.prefix}-${var.temp-dynamo-table-name}"
  dynamo_ppg  = "${var.prefix}-${var.ppg-dynamo-table-name}"
}

resource "aws_dynamodb_table" "ppg_fd2s_history" {
  name           = local.dynamo_ppg
  hash_key       = "DeviceId"
  range_key      = "Date"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5

  attribute {
    name = "DeviceId"
    type = "S"
  }

  attribute {
    name = "Date"
    type = "S"
  }

  tags = {
    project = var.prj_code
    dept    = var.data_dept
    env     = var.env
  }
}

resource "aws_dynamodb_table" "temp_fd2s_history" {
  name           = local.dynamo_temp
  hash_key       = "DeviceId"
  range_key      = "Date"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5

  attribute {
    name = "DeviceId"
    type = "S"
  }

  attribute {
    name = "Date"
    type = "S"
  }

  tags = {
    project = var.prj_code
    dept    = var.data_dept
    env     = var.env
  }
}
