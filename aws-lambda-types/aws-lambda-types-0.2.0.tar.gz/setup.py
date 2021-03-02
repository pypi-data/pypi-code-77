# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_lambda_types']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'aws-lambda-types',
    'version': '0.2.0',
    'description': 'Type definitions for AWS Lambda events using Python type hinting.',
    'long_description': '# aws-lambda-py-types\n\n[![Test](https://github.com/emcpow2/aws-lambda-py-types/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/emcpow2/aws-lambda-py-types/actions/workflows/main.yml)\n\nType definitions for AWS Lambda events using Python type hinting.\n\n## A Simple Example\n\n```py\nfrom aws_lambda_types.sns import SNSEventDict\n\n\ndef lambda_handler(event: SNSEventDict, context):\n    message = event["Records"][0]["Sns"]["Message"]\n    print("From SNS: " + message)\n    return message\n```\n\n![usage.gif](./docs/usage.gif)\n\n## Useful documentation\n\n- [Application Load Balancers - Lambda functions as targets](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/lambda-functions.html)\n- [Using AWS Lambda with Amazon SNS](https://docs.aws.amazon.com/lambda/latest/dg/with-sns.html)\n- [Working with AWS Lambda proxy integrations for HTTP APIs](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html)\n',
    'author': 'Eduard Iskandarov',
    'author_email': 'eduard.iskandarov@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/emcpow2/aws-lambda-py-types',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
