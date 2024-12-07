terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "totes-project-tfstate-backend-2"
    key    = "totes-tfstate/terraform.tfstate"
    region = "eu-west-2"
  }
}

provider "aws" {
  region = "eu-west-2"

  default_tags {
    tags = { project = "totes-project" }
  }
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

resource "aws_cloudwatch_log_group" "load_log_group" {
  name              = "/aws/lambda/load_handler"
  retention_in_days = 0
}


resource "aws_cloudwatch_log_group" "transform_log_group" {
  name              = "/aws/lambda/transform_handler"
  retention_in_days = 0
}

resource "aws_cloudwatch_log_group" "extract_log_group" {
  name              = "/aws/lambda/extract_handler"
  retention_in_days = 0
}

