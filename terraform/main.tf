locals {
  lib_filename        = "adbounty_lib.zip"
  domain-name         = "ad-bounty.com"
  website-bucket-name = "adbounty-website-artifact-bucket"
  code-bucket-name    = "adbounty-lambda-code-bucket"
  account-id          = "748004005034"
  region              = "us-east-1"
}


provider "aws" {
  profile = "default"
  region  = "us-east-1"
  version = "2.57.0"
}

##############
##API Section


# API Gateway
resource "aws_api_gateway_rest_api" "api" {
  name = "ad-bounty-api"
}

resource "aws_api_gateway_deployment" "deployment" {
  description = "Deployed from Terraform on ${timestamp()}"
  rest_api_id = aws_api_gateway_rest_api.api.id
  stage_name  = "prod"
  # force redeploy:
  variables = {
    deployed_at = "${timestamp()}"
  }
}

resource "aws_api_gateway_resource" "resource" {
  path_part   = "{object+}"
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  rest_api_id = aws_api_gateway_rest_api.api.id
}

resource "aws_api_gateway_method" "method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.resource.id
  http_method   = "GET"
  authorization = "NONE"
  request_parameters = {
    "method.request.path.object" = true
  }
}

resource "aws_api_gateway_integration" "integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.resource.id
  http_method             = aws_api_gateway_method.method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.youtube_puller_lambda.invoke_arn
  request_parameters = {
    "integration.request.path.object" = "method.request.path.object"
  }
}

resource "aws_api_gateway_method_response" "response_200" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.resource.id
  http_method = aws_api_gateway_method.method.http_method
  status_code = "200"
}

resource "aws_lambda_permission" "apigw_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.youtube_puller_lambda.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "arn:aws:execute-api:${local.region}:${local.account-id}:${aws_api_gateway_rest_api.api.id}/*/${aws_api_gateway_method.method.http_method}${aws_api_gateway_resource.resource.path}"
}



resource "aws_lambda_function" "youtube_puller_lambda" {
  s3_bucket        = "adbounty-lambda-code-bucket"
  s3_key           = "youtube_puller.zip"
  function_name    = "youtube-puller"
  role             = aws_iam_role.iam_for_lambda_default.arn
  handler          = "lambdas/youtube_puller.handler"
  layers           = [aws_lambda_layer_version.lib_layer.arn]
  runtime          = "python3.8"
  source_code_hash = filebase64sha256("../lambdas_compiled/youtube_puller.zip")
  timeout          = 60 # timeout in seconds. 
  memory_size      = 256
  environment {
    variables = {
      "SECRET_ID" = "${aws_secretsmanager_secret.youtube-cred.id}"
    }
  }
}

resource "aws_secretsmanager_secret" "youtube-cred" {
  name = "youtube-cred"
}

resource "aws_iam_role" "iam_for_lambda_default" {
  name = "iam_for_youtube_puller_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy" "lambda_secrets_manager_access" {
  name        = "iam_for_lambda_secrets_access"
  path        = "/"
  description = "IAM policy for lambda to access secrets manager"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "secretsmanager:GetResourcePolicy",
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret",
        "secretsmanager:ListSecretVersionIds"
      ],
      "Resource": "${aws_secretsmanager_secret.youtube-cred.arn}",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_secrets_manager_attach" {
  role       = aws_iam_role.iam_for_lambda_default.name
  policy_arn = aws_iam_policy.lambda_secrets_manager_access.arn
}


resource "aws_lambda_layer_version" "lib_layer" {
  s3_bucket  = local.code-bucket-name
  s3_key     = local.lib_filename
  layer_name = "chainlink-lambda-libs"

  compatible_runtimes = ["python3.7"]
}




#######
#  Website Hosting section
######





resource "aws_cloudfront_distribution" "website_distribution" {
  origin {
    domain_name = "${local.website-bucket-name}.s3.amazonaws.com"
    origin_id   = "${local.domain-name}-s3-origin"
  }
  aliases = [local.domain-name]

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "${local.domain-name}-s3-origin"

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "allow-all"
    min_ttl                = 0
    default_ttl            = 86400
    max_ttl                = 31536000
  }
  enabled         = true
  is_ipv6_enabled = true
  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate.website_cert.arn
    minimum_protocol_version = "TLSv1.1_2016"
    ssl_support_method       = "sni-only"
  }

  custom_error_response {
    error_caching_min_ttl = 300
    error_code            = 403
    response_code         = 200
    response_page_path    = "/index.html"
  }

  custom_error_response {
    error_caching_min_ttl = 300
    error_code            = 404
    response_code         = 200
    response_page_path    = "/index.html"
  }
  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
}


resource "aws_route53_record" "website_record_a" {
  zone_id = aws_route53_zone.website_zone.zone_id
  name    = local.domain-name
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.website_distribution.domain_name
    zone_id                = aws_cloudfront_distribution.website_distribution.hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "website_record_aaaa" {
  zone_id = aws_route53_zone.website_zone.zone_id
  name    = local.domain-name
  type    = "AAAA"

  alias {
    name                   = aws_cloudfront_distribution.website_distribution.domain_name
    zone_id                = aws_cloudfront_distribution.website_distribution.hosted_zone_id
    evaluate_target_health = false
  }
}


resource "aws_route53_zone" "website_zone" {
  name    = local.domain-name
  comment = "HostedZone created by Route53 Registrar"
}


resource "aws_s3_bucket" "website_bucket" {
  bucket = local.website-bucket-name
  acl    = "private"
  website {
    error_document = "index.html"
    index_document = "index.html"
  }
}
resource "aws_s3_bucket" "code_bucket" {
  bucket = local.code-bucket-name
  acl    = "private"
}

resource "aws_acm_certificate" "website_cert" {
  domain_name       = local.domain-name
  validation_method = "DNS"
}


