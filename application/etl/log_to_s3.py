
import logging
import os
import boto3
from botocore.exceptions import ClientError
from get_secrets import get_secrets_manager_values

def send_etl_logs() -> str:
 
    secrets = get_secrets_manager_values()

    try:
        s3_client = boto3.client('s3')
        log_file_path = logging.getLogger().handlers[0].baseFilename  # Get the log file path
        log_filename = os.path.basename(log_file_path)

        bucket_name = secrets['BUCKET_NAME']  # Ensure this is in your secrets
        
        s3_key = f"logs/glue-job/{log_filename}"  # Adjust the path as needed
        
        s3_client.upload_file(log_file_path, bucket_name, s3_key) 
    except ClientError as ce:
        print(f'something wrong with aws s3 connection: {ce}')
    except Exception as e:
        print(f'error when sending to s3 {e}') 