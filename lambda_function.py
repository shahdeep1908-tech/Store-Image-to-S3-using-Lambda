import uuid

import boto3
import os
import urllib
from PIL import Image

s3 = boto3.client('s3')
ses = boto3.client('ses')


def lambda_handler(event, context):
    for record in event['Records']:
        # Extract S3 bucket and key details for the uploaded object
        bucket = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'])

        # Get the size of the uploaded object
        obj = s3.get_object(Bucket=bucket, Key=key)
        size = obj['ContentLength']

        # Get the content type of the uploaded object
        content_type = obj['ContentType']

        # Extract object name from the S3 key
        object_name = os.path.basename(key)

        # Check if uploaded object is an image
        if 'image' in content_type:
            # Generate thumbnail and store it in a different S3 bucket
            generate_thumbnail(bucket, key)

        # Send email with details to select users
        send_email(bucket, key, object_name, size, content_type)


def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        image.thumbnail(tuple(x / 2 for x in image.size))
        image.save(resized_path)


def generate_thumbnail(bucket, key):
    s3_resource = boto3.resource('s3')
    object = s3_resource.Object(bucket, key)

    # Use Pillow library to generate thumbnail
    tmpkey = key.replace('/', '')
    download_path = f'/tmp/{uuid.uuid4()}{tmpkey}'
    upload_path = f'/tmp/resized-{tmpkey}'
    s3.download_file(bucket, key, download_path)
    resize_image(download_path, upload_path)
    destination_bucket = "aws-s3-ses-assignment-thumbnail-bucket"
    s3.upload_file(upload_path, destination_bucket, key)


def send_email(bucket, key, object_name, size, content_type):
    # Construct email message with object details
    subject = 'New object uploaded to S3'
    body = f'S3 Uri: s3://{bucket}/{key}\nObject Name: {object_name}\nObject Size: {size} bytes\nObject Type: {content_type}'
    sender = "['sender']@gmail.com"
    recipients = ["['recipient-1']@gmail.com", "['recipient-2']@gmail.com", ]

    # Send email using Amazon SES
    response = ses.send_email(
        Source=sender,
        Destination={
            'ToAddresses': recipients
        },
        Message={
            'Subject': {
                'Data': subject
            },
            'Body': {
                'Text': {
                    'Data': body
                }
            }
        }
    )
