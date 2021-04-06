variable "prefix" {
  description = "Common resource prefix"
  type        = string
  default     = "empatica"
}

variable "model-x-bucket-name" {
  description = "Bucket id for the bucket containing data from the model X wearable device"
  type        = string
  default     = "model-x"
}

variable "code-bucket-name" {
  description = "Bucket id for the code"
  type        = string
  default     = "artifactory"
}

variable "s3-logs-bucket-name" {
  description = "Bucket id for the bucket containing S3 logs"
  type        = string
  default     = "s3-logs"
}

variable "temp-dynamo-table-name" {
  description = "Dynamo table name temp"
  type        = string
  default     = "temp_fd2s_history"
}

variable "ppg-dynamo-table-name" {
  description = "Dynamo table name PPG"
  type        = string
  default     = "ppg_fd2s_history"
}

variable "prj_code" {
  description = "Project code for model X faulty device detection"
  type        = string
  default     = "PJ-XYZW"
}

variable "data_dept" {
  description = "Empatica department name for data"
  type        = string
  default     = "data"
}

variable "env" {
  description = "Empatica environment type"
  type        = string
  default     = "dev"
}

variable "profile" {
  description = "AWS credentials profile"
  type        = string
  default     = "empatica"
}

variable "region" {
  description = "AWS credentials region"
  type        = string
  default     = "eu-central-1"
}
