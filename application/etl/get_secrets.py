
import boto3
from botocore.exceptions import ClientError
import json

def get_secrets_manager_values() -> dict:
    """fetch data on AWS Secrets Manager secrets storad in a dictionary in the cloud and return it"""
    secret_repo_name = "secret-variables/anime-analytics"   # i have no solution yet for  
    secrets_repo_region_name = "eu-central-1"               # this except uploading 
                                                            # a json file to S3 for glue
                                                            # to fetch from during execution
    try:
        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=secrets_repo_region_name
        )
    except ClientError as ce:
        raise f'could not connect to boto3 client: {ce}'

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_repo_name
        )
        secret = get_secret_value_response['SecretString']
        json_secret = json.loads(secret)
        return json_secret

    except ClientError as ce:
        raise f'could not find any secrets as key-value stored in secrets-manager: {ce}'
    except Exception as e:
        raise e
    
if __name__ == '__main__':
    get_secrets_manager_values()

    