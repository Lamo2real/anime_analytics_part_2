import pandas as pd 

from extract_data_s3 import s3_data_extract

def divide_dataframe():
    """create three dataframes of the one big table from S3 data lake"""
    try:
        raw_df = s3_data_extract()
        data_type_converter(raw_df)

    except Exception as e:
        raise Exception(f'something unexpected went wrong: {e}')
    


    
def data_type_converter(dataframe) -> pd.DataFrame:
    """convert the datatypes for each column and convert it to the data model's datatype"""

    print(f'before converting datatypes:\n{dataframe.dtypes}')
    dataframe.to_csv('original_anime_data.csv')
    try:
        for column in ['episodes', 'duration', 'studio_id', 'genre_id_1', 'genre_id_2', 'genre_id_3']:
            dataframe[column] = pd.to_numeric(dataframe[column], errors='coerce').round().astype('Int64')

        print(f'after converting datatypes:\n{dataframe.dtypes}')
        dataframe.to_csv('processed_anime_data.csv')

        return dataframe
    
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise e

if __name__ == '__main__':
    divide_dataframe()
