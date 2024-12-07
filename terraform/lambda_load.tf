data "archive_file" "load_function" {
  type             = "zip"
  output_file_mode = "0666"
  source_dir       = "${path.module}/../src"
  output_path      = "${path.module}/../zip_funcs/load.zip"
}

resource "aws_lambda_function" "load_lambda" {
  function_name = "load_handler"             # await python handler name
  handler       = "load.lambda_handler_load" # await python handler name
  runtime       = "python3.12"
  s3_bucket     = aws_s3_bucket.code_bucket.bucket
  s3_key        = "load/load.zip"
  timeout       = 180
  role          = aws_iam_role.load_lambda_role.arn
  layers        = ["${aws_lambda_layer_version.lambdas_layer.arn}"]
  depends_on    = [aws_s3_object.load_lambda_code]
  memory_size   = 256

  source_code_hash = data.archive_file.load_function.output_base64sha256

  logging_config {
    log_format = "Text"
    log_group  = aws_cloudwatch_log_group.load_log_group.name
  }

  environment {
    variables = {
      S3_TRANSFORM_BUCKET_NAME = aws_s3_bucket.transform_bucket.bucket
    }
  }
  tags = {
    description = "takes data from the transform bucket and stores it in the warehouse"
  }
}

# adding the code from the load lambda (zip) to the code bucket
resource "aws_s3_object" "load_lambda_code" {
  bucket     = aws_s3_bucket.code_bucket.bucket
  key        = "load/load.zip"
  source     = data.archive_file.load_function.output_path
  depends_on = [data.archive_file.load_function]
  etag       = filemd5(data.archive_file.load_function.output_path)
}
