#Lambda IAM Role(s)
#------------------

# Define
data "aws_iam_policy_document" "extract_lambda_trust_policy" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

# Create
resource "aws_iam_role" "extract_lambda_role" {
  name_prefix        = "role-extract-lambda"
  assume_role_policy = data.aws_iam_policy_document.extract_lambda_trust_policy.json
}


# IAM Policy Documents
# --------------------
data "aws_iam_policy_document" "s3_landing_write_policy_doc" {
  statement {
    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.landing_bucket.arn}/*"]
  }
  statement {
    actions   = ["s3:ListBucket"]
    resources = ["${aws_s3_bucket.landing_bucket.arn}"]
  }
}

data "aws_iam_policy_document" "cw_policy_doc" {
  statement {
    actions   = ["logs:CreateLogStream", "logs:PutLogEvents"]
    resources = ["arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:*:log-stream:*"]
  }
}

data "aws_iam_policy_document" "extract_lambda_get_secret_doc" {
  statement {
    actions   = ["secretsmanager:GetSecretValue"]
    resources = ["arn:aws:secretsmanager:eu-west-2:699475945437:secret:totesys_db_credentials-uDzvZf"]
  }

}


# IAM Policies
# ------------
resource "aws_iam_policy" "s3_landing_write_policy" {
  name_prefix = "s3-landing-write-policy-"
  policy      = data.aws_iam_policy_document.s3_landing_write_policy_doc.json
}

resource "aws_iam_policy" "cw_policy" {
  name_prefix = "cw-policy-"
  policy      = data.aws_iam_policy_document.cw_policy_doc.json
}

resource "aws_iam_policy" "extract_lambda_get_secret_policy" {
  name_prefix = "extract-lambda-get-secret-policy-"
  policy      = data.aws_iam_policy_document.extract_lambda_get_secret_doc.json
}



# IAM Policy Attachments
# ----------------------

# Extract Policy Attachments
resource "aws_iam_role_policy_attachment" "s3_landing_write_policy_attachment" {
  role       = aws_iam_role.extract_lambda_role.name
  policy_arn = aws_iam_policy.s3_landing_write_policy.arn
}

resource "aws_iam_role_policy_attachment" "extract_lambda_cw_policy_attachment" {
  role       = aws_iam_role.extract_lambda_role.name
  policy_arn = aws_iam_policy.cw_policy.arn
}

resource "aws_iam_role_policy_attachment" "extract_lambda_get_secret_policy_attachment" {
  role       = aws_iam_role.extract_lambda_role.name
  policy_arn = aws_iam_policy.extract_lambda_get_secret_policy.arn
}

