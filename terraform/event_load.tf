#Creates scheduler to run every 15 mins
resource "aws_cloudwatch_event_rule" "load_scheduler" {
  name                = "load_scheduler"
  description         = "runs load lambda every 15 minutes"
  schedule_expression = "cron(5/15 * * * ? *)"
}

#Sets load lambda as the target of the scheduler 
resource "aws_cloudwatch_event_target" "load_scheduler_target" {
  rule      = aws_cloudwatch_event_rule.load_scheduler.name
  arn       = aws_lambda_function.load_lambda.arn
  target_id = "load_lambda"
}

#Permission for scheduler to execute load lambda function
resource "aws_lambda_permission" "allow_cloudwatch_events_load" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.load_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.load_scheduler.arn
}

#filters cloudwatch logs to find instances of ERROR, then increases the value count to record an ERROR has occurred
resource "aws_cloudwatch_log_metric_filter" "load_error_filter" {
  name           = "load_error_count"
  log_group_name = "/aws/lambda/load_handler"
  pattern        = "?ERROR ?FAILURE"
  depends_on = [ aws_cloudwatch_log_group.load_log_group ]

  metric_transformation {
    name      = "load_error_count"
    namespace = "load_errors"
    value     = "1"
  }
}


#creates sns topic for error occurences in extract function
resource "aws_sns_topic" "load_error_topic" {
  name = "load-error-emails"
}

#topic policy document
data "aws_iam_policy_document" "load_error_topic_policy_doc" {
  statement {
    effect  = "Allow"
    actions = ["SNS:Publish"]

    principals {
      type        = "Service"
      identifiers = ["cloudwatch.amazonaws.com"]
    }

    resources = [aws_sns_topic.load_error_topic.arn]
  }
}

#policy for topic/sns service
resource "aws_sns_topic_policy" "load_error_topic_policy" {
  arn    = aws_sns_topic.load_error_topic.arn
  policy = data.aws_iam_policy_document.load_error_topic_policy_doc.json
}

#creates email subscription for load error topic
resource "aws_sns_topic_subscription" "load_email_subscription" {
  topic_arn = aws_sns_topic.load_error_topic.arn
  protocol  = "email"
  endpoint  = var.email_endpoint
}
# checks filter periodically, records to topic and triggers sns event
resource "aws_cloudwatch_metric_alarm" "load_error_alarm" {
  alarm_name          = "load_error_alarm"
  metric_name         = aws_cloudwatch_log_metric_filter.load_error_filter.name
  threshold           = 0
  statistic           = "Sum"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  period              = "60"
  namespace           = "load_errors"
  alarm_description   = "Triggers when an ERROR is logged"
  alarm_actions       = [aws_sns_topic.load_error_topic.arn]

  depends_on = [aws_cloudwatch_log_metric_filter.load_error_filter,
    aws_sns_topic.load_error_topic,
    aws_sns_topic_policy.load_error_topic_policy,
    aws_sns_topic_subscription.load_email_subscription
  ]
}
