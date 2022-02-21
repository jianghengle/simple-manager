# Invoice email receiver
It is a lambda function runinng every time the invoice@vanityart.com receive an email. As you can see from the source code, it will:
1. Reads the email message from S3
2. Determines if it is an invoice email
3. Collects info and `overrides`
4. Saves the attachments to S3
5. Calls `django-rest` API to create the invoice

## Development
Can only run the script in lambda. So if you make some change, you need to deploy it to test.

## Deployment
Open AWS console and find the lambda function `invoice-receiver`

Copy the content of `lambda_function.py` into the Code source `lambda_function.py`.
