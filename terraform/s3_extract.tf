# bucket created to store code
resource "aws_s3_bucket" "code_bucket" {
  bucket_prefix = "totes-code-"
  tags = {
    name = "bucket_for_lambda_code"
  }
}

# bucket to store the landing data extracted by the first lambda (ingest)
resource "aws_s3_bucket" "landing_bucket" {
  bucket_prefix = "totes-landing-data-"
  tags = {
    name = "bucket_for_landing_totesys_data"
  }
}

# adding the code from the ingest lambda (zip) to the code bucket
resource "aws_s3_object" "extract_lambda_code" {
  bucket     = aws_s3_bucket.code_bucket.bucket
  key        = "extract/extract.zip"
  source     = data.archive_file.extract_function.output_path
  depends_on = [data.archive_file.extract_function]
  etag       = filemd5(data.archive_file.extract_function.output_path)
}

# adding the code from the layer (zip) to the code bucket
resource "aws_s3_object" "layer_code" {
  bucket     = aws_s3_bucket.code_bucket.bucket
  key        = "lambda_layers/lambdas_layer.zip"
  source     = data.archive_file.lambdas_layer.output_path
  depends_on = [data.archive_file.lambdas_layer]
  etag       = filemd5(data.archive_file.lambdas_layer.output_path)
}


