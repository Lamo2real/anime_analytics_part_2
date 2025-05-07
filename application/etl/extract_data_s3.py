import boto3
from botocore.exceptions import ClientError
import pandas as pd
from get_secrets import get_secrets_manager_values
import logging
from logger_setup import setup_logger
setup_logger()


logger = logging.getLogger(__name__)

def s3_data_extract() -> pd.DataFrame:
    """
    get environment vars and call for the fetch_s3_dataframe function,
    which returns a pandas dataframe which will be returned here.
    """

    try:
        secrets = get_secrets_manager_values()
        return fetch_s3_dataframe(secrets['BUCKET_NAME'], secrets['FILE_PATH'])
    
    except FileNotFoundError as fnfe:
        logger.error(f'could not find the file to get secrets: {fnfe}', exc_info=True)
        raise 
    except ImportError as ie:
        logger.error(f'could not import the secrets file: {ie}', exc_info=True)
        raise 
    except Exception as e:
        logger.critical(f'something unexpected went wrong {e}', exc_info=True)
        raise
    

    
    
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
        logger.error(f'could not connect or other issues with s3 client: {ce}', exc_info=True)
        raise
    except Exception as e:
        logger.critical(f'something else went wrong: {e}', exc_info=True)
        raise
        

