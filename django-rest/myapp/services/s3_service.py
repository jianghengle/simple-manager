import logging
import boto3
from botocore.exceptions import ClientError
from django.conf import settings

def get_s3_client():
    s3_client = boto3.client('s3',
                              aws_access_key_id=settings.ACCESS_KEY_ID,
                              aws_secret_access_key=settings.SECRET_ACCESS_KEY)
    return s3_client

def create_presigned_post(bucket_name, object_name,
                          fields=None, conditions=None, expiration=3600):
    """Generate a presigned URL S3 POST request to upload a file

    :param bucket_name: string
    :param object_name: string
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """

    # Generate a presigned S3 POST URL
    s3_client = get_s3_client()
    try:
        response = s3_client.generate_presigned_post(bucket_name,
                                                     object_name,
                                                     Fields=fields,
                                                     Conditions=conditions,
                                                     ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response

def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = get_s3_client()
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response

def download_file(file_path, bucket, key):
    s3_client = get_s3_client()
    s3_client.download_file(bucket, key, file_path)

def upload_file(file_path, bucket, key):
    s3_client = get_s3_client()
    s3_client.upload_file(file_path, bucket, key)

def copy_object(source_bucket, source_key, target_bucket, target_key):
    s3_client = get_s3_client()
    copy_source = {
        'Bucket': source_bucket,
        'Key': source_key
    }
    s3_client.copy(copy_source, target_bucket, target_key)

def get_object_content(bucket, key):
    s3_client = get_s3_client()
    s3_object = s3_client.get_object(Bucket=bucket, Key=key)
    return s3_object['Body'].read()
