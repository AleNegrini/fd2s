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
