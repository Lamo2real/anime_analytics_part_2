import boto3
from botocore.exceptions import ClientError
import pandas as pd
# import logging
from get_secrets import get_secrets_manager_values

# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s %(levelname)s %(message)s',
#     datefmt='%Y-%m-%d %H:%M',
#     filename='etl-pipeline-logs.log'
# )


def s3_data_extract() -> pd.DataFrame:
    """
    get environment vars and call for the fetch_s3_dataframe function,
    which returns a pandas dataframe which will be returned here.
    """

    try:
        secrets = get_secrets_manager_values()
        return fetch_s3_dataframe(secrets['BUCKET_NAME'], secrets['FILE_PATH'])
    
    except FileNotFoundError as fnfe:
        print(f'could not find the file to get secrets')
        raise fnfe
    except ImportError as ie:
        print(f'could not import the secrets file')
        raise ie
    except Exception as e:
        print(f'something unexpected went wrong {e}')
    

    
    
def fetch_s3_dataframe(bucket_name, file_path) -> pd.DataFrame:
    """
    try to get csv object from data lake in s3 and retun it as a pandas dataframe
    """
    
    try:
        client = boto3.client('s3')
        file = client.get_object(Bucket=bucket_name, Key=file_path)
        if file:
            data = file['Body']
            dataframe = pd.read_csv(data)
            return dataframe

    except ClientError as ce:
        raise ClientError(f'could not connect or other issues with s3 client: {ce}')
    except Exception as e:
        raise Exception(f'something else went wrong: {e}')
        

if __name__ == '__main__':
    s3_data_extract()
