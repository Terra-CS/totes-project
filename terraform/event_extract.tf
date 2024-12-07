#Creates scheduler to run every 15 mins
resource "aws_cloudwatch_event_rule" "extract_scheduler" {
  name                = "extract_scheduler"
  description         = "runs extract lambda every 15 minutes"
  schedule_expression = "cron(0/15 * * * ? *)"
}

#Sets extract lambda as the target of the scheduler 
resource "aws_cloudwatch_event_target" "extract_scheduler_target" {
  rule      = aws_cloudwatch_event_rule.extract_scheduler.name
  arn       = aws_lambda_function.extract_lambda.arn
  target_id = "extract_lambda"
}

#Permission for scheduler to execute extract lambda function
resource "aws_lambda_permission" "allow_cloudwatch_events" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.extract_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.extract_scheduler.arn
}

#filters cloudwatch logs to find instances of ERROR, then increases the value count to record an ERROR has occurred
resource "aws_cloudwatch_log_metric_filter" "extract_error_filter" {
  name           = "extract_error_count"
  log_group_name = "/aws/lambda/extract_handler"
  pattern        = "?ERROR ?FAILURE"
  depends_on     = [aws_cloudwatch_log_group.extract_log_group]

  metric_transformation {
    name      = "extract_error_count"
    namespace = "extract_errors"
    value     = "1"
  }

}

#creates sns topic for error occurences in extract function
resource "aws_sns_topic" "extract_error_topic" {
  name = "extract-error-emails"
}

#topic policy document
data "aws_iam_policy_document" "extract_error_topic_policy_doc" {
  statement {
    effect  = "Allow"
    actions = ["SNS:Publish"]

    principals {
      type        = "Service"
      identifiers = ["cloudwatch.amazonaws.com"]
    }

    resources = [aws_sns_topic.extract_error_topic.arn]
  }
}

#policy for topic/sns service
resource "aws_sns_topic_policy" "extract_error_topic_policy" {
  arn    = aws_sns_topic.extract_error_topic.arn
  policy = data.aws_iam_policy_document.extract_error_topic_policy_doc.json
}

#creates email subscription for extract error topic
resource "aws_sns_topic_subscription" "extract_email_subscription" {
  topic_arn = aws_sns_topic.extract_error_topic.arn
  protocol  = "email"
  endpoint  = var.email_endpoint
}

#checks filter periodically, records to topic and triggers sns event
resource "aws_cloudwatch_metric_alarm" "extract_error_alarm" {
  alarm_name          = "extract_error_alarm"
  metric_name         = aws_cloudwatch_log_metric_filter.extract_error_filter.name
  threshold           = 0
  statistic           = "Sum"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  period              = "60"
  namespace           = "extract_errors"
  alarm_description   = "Triggers when an ERROR is logged"
  alarm_actions       = [aws_sns_topic.extract_error_topic.arn]

  depends_on = [aws_cloudwatch_log_metric_filter.extract_error_filter,
    aws_sns_topic.extract_error_topic,
    aws_sns_topic_policy.extract_error_topic_policy,
    aws_sns_topic_subscription.extract_email_subscription
  ]
}
