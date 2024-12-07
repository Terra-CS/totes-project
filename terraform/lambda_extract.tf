data "archive_file" "extract_function" {
  type             = "zip"
  output_file_mode = "0666"
  source_dir       = "${path.module}/../src"
  output_path      = "${path.module}/../zip_funcs/extract.zip"
}

resource "aws_lambda_function" "extract_lambda" {
  function_name = "extract_handler"
  handler       = "ingest.lambda_handler_ingestion"
  runtime       = "python3.12"
  s3_bucket     = aws_s3_bucket.code_bucket.bucket
  s3_key        = "extract/extract.zip"
  timeout       = 180
  role          = aws_iam_role.extract_lambda_role.arn
  layers        = ["${aws_lambda_layer_version.lambdas_layer.arn}"]
  depends_on    = [aws_s3_object.extract_lambda_code]
  memory_size   = 256

  source_code_hash = data.archive_file.extract_function.output_base64sha256

  logging_config {
    log_format = "Text"
    log_group  = aws_cloudwatch_log_group.extract_log_group.name
  }

  environment {
    variables = {
      S3_LANDING_BUCKET_NAME = aws_s3_bucket.landing_bucket.bucket
    }
  }
  tags = {
    description = "takes data from the totesys db and stores it in the s3 landing bucket"
  }
}

data "archive_file" "lambdas_layer" {
  type             = "zip"
  output_file_mode = "0666"
  source_dir       = "${path.module}/../lambdas_layer"
  output_path      = "${path.module}/../zip_funcs/lambdas_layer.zip"
}

resource "aws_lambda_layer_version" "lambdas_layer" {
  layer_name          = "lambdas_layer"
  compatible_runtimes = ["python3.12"]
  s3_bucket           = aws_s3_bucket.code_bucket.bucket
  s3_key              = aws_s3_object.layer_code.key
}

