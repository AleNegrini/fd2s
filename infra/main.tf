provider "aws" {
  region  = "eu-central-1"
  profile = "empatica"
}

terraform {
  backend "s3" {
    bucket  = "empatica-tf-states"
    key     = "fd2s"
    region  = "eu-central-1"
    profile = "empatica"
  }
}
