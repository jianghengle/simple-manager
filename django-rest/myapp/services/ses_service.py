import boto3
from botocore.exceptions import ClientError
from django.conf import settings

SENDER = "Vanityart Invoice System <invoice-system@vanityart.com>"

AWS_REGION = "us-east-1"        

CHARSET = "UTF-8"

def send_email(recipents, subject, body_text, body_html):
    client = boto3.client('ses',
                          aws_access_key_id=settings.ACCESS_KEY_ID, 
                          aws_secret_access_key=settings.SECRET_ACCESS_KEY,
                          region_name=AWS_REGION)
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': recipents,
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': body_html,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': subject,
                },
            },
            Source=SENDER,
        )

    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])