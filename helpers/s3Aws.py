import boto3
from flask import send_file
import os

import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

#AWS IAM credentials
aws_access_key_id = os.getenv('aws_access_key_id')
aws_secret_access_key = os.getenv('aws_secret_access_key')
region_name = os.getenv('region_name')
bucketName = os.getenv('bucketName')

# Create S3 client
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)


#Upload image to Bucket
def uploadImage(filename):    
    try:
        s3.upload_file(filename, bucketName, filename)
        print(f'Successfully uploaded {filename} to {bucketName}')
    except Exception as e:
        print(f'Error uploading {filename} to {bucketName}: {str(e)}')

#Delete image from the Bucket
def deleteImage(filename):
    try:
        s3.delete_object(Bucket=bucketName, Key=filename)
        print(f'Successfully deleted {filename} from {bucketName}')

    except Exception as e:
        print(f'Error deleting {filename} from {bucketName}: {str(e)}')

#Get image image from the Bucket
def getImage(filename, destination_path):
    try:
        s3.download_file(bucketName, filename, destination_path)
        print(f'Successfully downloaded {filename} to {destination_path}')
        return send_file(destination_path, as_attachment=True)
    except Exception as e:
        nerror= f'Error downloading {filename} from {bucketName}: {str(e)}'
        return nerror
