# bucket to store the landing data extracted by the second lambda (transform)
resource "aws_s3_bucket" "transform_bucket" {
  bucket_prefix = "totes-transform-data-"
  tags = {
    name = "bucket_for_transformed_data_from_second_lambda"
  }
}


# adding the code from the transform lambda (zip) to the code bucket
resource "aws_s3_object" "transform_lambda_code" {
  bucket     = aws_s3_bucket.code_bucket.bucket
  key        = "transform/transform.zip"
  source     = data.archive_file.transform_function.output_path
  depends_on = [data.archive_file.transform_function]
  etag       = filemd5(data.archive_file.transform_function.output_path)
}

