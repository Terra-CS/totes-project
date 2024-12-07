#filters cloudwatch logs to find instances of ERROR, then increases the value count to record an ERROR has occurred
resource "aws_cloudwatch_log_metric_filter" "transform_error_filter" {
  name           = "transform_error_count"
  log_group_name = "/aws/lambda/transform_handler"
  pattern        = "?ERROR ?FAILURE"
  depends_on     = [aws_cloudwatch_log_group.transform_log_group]

  metric_transformation {
    name      = "transform_error_count"
    namespace = "transform_errors"
    value     = "1"
  }
}


#creates sns topic for error occurences in extract function
resource "aws_sns_topic" "transform_error_topic" {
  name = "transform-error-emails"
}

#topic policy document
data "aws_iam_policy_document" "transform_error_topic_policy_doc" {
  statement {
    effect  = "Allow"
    actions = ["SNS:Publish"]

    principals {
      type        = "Service"
      identifiers = ["cloudwatch.amazonaws.com"]
    }

    resources = [aws_sns_topic.transform_error_topic.arn]
  }
}

#policy for topic/sns service
resource "aws_sns_topic_policy" "transform_error_topic_policy" {
  arn    = aws_sns_topic.transform_error_topic.arn
  policy = data.aws_iam_policy_document.transform_error_topic_policy_doc.json
}

#creates email subscription for transform error topic
resource "aws_sns_topic_subscription" "transform_email_subscription" {
  topic_arn = aws_sns_topic.transform_error_topic.arn
  protocol  = "email"
  endpoint  = var.email_endpoint
}
# checks filter periodically, records to topic and triggers sns event
resource "aws_cloudwatch_metric_alarm" "transform_error_alarm" {
  alarm_name          = "transform_error_alarm"
  metric_name         = aws_cloudwatch_log_metric_filter.transform_error_filter.name
  threshold           = 0
  statistic           = "Sum"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  period              = "60"
  namespace           = "transform_errors"
  alarm_description   = "Triggers when an ERROR is logged"
  alarm_actions       = [aws_sns_topic.transform_error_topic.arn]

  depends_on = [aws_cloudwatch_log_metric_filter.transform_error_filter,
    aws_sns_topic.transform_error_topic,
    aws_sns_topic_policy.transform_error_topic_policy,
    aws_sns_topic_subscription.transform_email_subscription
  ]
}
