locals {
  data_bucket_name = "${var.prefix}-${var.model-x-bucket-name}"
  code_bucket_name = "${var.prefix}-${var.code-bucket-name}"
}

resource "aws_s3_bucket" "empatica-signals-model-X" {
  bucket = local.data_bucket_name
  acl    = "private"

  tags = {
    project = var.prj_code
    dept    = var.data_dept
    env     = var.env
  }
}

resource "aws_s3_bucket" "empatica-artifactory" {
  bucket = local.code_bucket_name
  acl    = "private"

  tags = {
    project = var.prj_code
    dept    = var.data_dept
    env     = var.env
  }
}

resource "aws_s3_bucket_object" "lambda_anomaly_orchestration" {

  bucket = "${aws_s3_bucket.empatica-artifactory.id}"
  key    = "anomaly_orchestration_dp.zip"
  source = "../code/anomaly_orchestration/src/anomaly_orchestration/anomaly_orchestration_dp.zip"

}

resource "aws_s3_bucket_object" "ppg_failure_detection" {

  bucket = "${aws_s3_bucket.empatica-artifactory.id}"
  key    = "ppg_failure_detection_dp.zip"
  source = "../code/ppg_failure_detection/src/ppg_failure_detection/ppg_failure_detection_dp.zip"

}

resource "aws_s3_bucket_object" "temp_failure_detection" {

  bucket = "${aws_s3_bucket.empatica-artifactory.id}"
  key    = "temp_failure_detection_dp.zip"
  source = "../code/wtemp_failure_detection/src/wtemp_failure_detection/temp_failure_detection_dp.zip"

}

resource "aws_s3_bucket_public_access_block" "model-x-block-public" {
  bucket = aws_s3_bucket.empatica-signals-model-X.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_public_access_block" "artifactory-block-public" {
  bucket = aws_s3_bucket.empatica-artifactory.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
