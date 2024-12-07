data "archive_file" "transform_function" {
  type             = "zip"
  output_file_mode = "0666"
  source_dir       = "${path.module}/../src"
  output_path      = "${path.module}/../zip_funcs/transform.zip"
}

resource "aws_lambda_function" "transform_lambda" {
  function_name = "transform_handler"
  handler       = "transform.lambda_handler_transform"
  runtime       = "python3.12"
  s3_bucket     = aws_s3_bucket.code_bucket.bucket
  s3_key        = "transform/transform.zip"
  timeout       = 180
  role          = aws_iam_role.transform_lambda_role.arn
  layers        = ["${aws_lambda_layer_version.lambdas_layer.arn}"]
  depends_on    = [aws_s3_object.transform_lambda_code]
  memory_size   = 256

  source_code_hash = data.archive_file.transform_function.output_base64sha256

  logging_config {
    log_format = "Text"
    log_group  = aws_cloudwatch_log_group.transform_log_group.name
  }

  environment {
    variables = {
      S3_LANDING_BUCKET_NAME   = aws_s3_bucket.landing_bucket.bucket
      S3_TRANSFORM_BUCKET_NAME = aws_s3_bucket.transform_bucket.bucket
    }
  }
  tags = {
    description = "takes data from the landing bucket and stores it in the transform bucket"
  }
}

# Adding S3 bucket as trigger to transform lambda and giving the permissions
resource "aws_s3_bucket_notification" "aws_lambda_trigger" {
  bucket = aws_s3_bucket.landing_bucket.id
  lambda_function {
    lambda_function_arn = aws_lambda_function.transform_lambda.arn
    events              = ["s3:ObjectCreated:*"]
  }
  depends_on = [aws_lambda_permission.landing_invoke_transform]
}

# Permission for lambda to be invoked by S3
resource "aws_lambda_permission" "landing_invoke_transform" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.transform_lambda.arn
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.landing_bucket.arn
}