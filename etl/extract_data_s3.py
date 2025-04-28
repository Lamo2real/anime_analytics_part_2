import boto3
from botocore.exceptions import ClientError
import pandas as pd
import os
from dotenv import load_dotenv



def s3_data_extract() -> pd.DataFrame:
    """
    get environment vars and call for the fetch_s3_dataframe function,
    which returns a pandas dataframe which will be returned here.
    """

    try:
        load_dotenv()
        s3 = {
            'bucket-name': os.environ.get('BUCKET_NAME'), # BUCKET NAME 
            'file-path': os.environ.get('FILE_PATH')      # PATH TO OBJECT FILE 
        } 
        print(f'the bucket name is {s3['bucket-name']}\nthe file path is: {s3['file-path']}')

    except FileNotFoundError as fnfe:
        print(f'the file wasnt found')
        raise fnfe

    except Exception as e:
        print(f'something else went wrong')
        raise e
    
    return fetch_s3_dataframe(s3['bucket-name'], s3['file-path'])

    
    
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