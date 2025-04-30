import pandas as pd 
from datetime import datetime

from extract_data_s3 import s3_data_extract
from snowflake_data_load import load_data_to_snoflake


def divide_dataframe():
    """create three dataframes of the one big table from S3 data lake"""

    try:
        raw_df = s3_data_extract() # extract data 

        ######### TRANSFORM DATA ##############
        clean_df = data_type_converter(raw_df)
        clean_df.insert(loc=7, column='is_current', value=clean_df['aired_to'].isna()) 
        dim_genre_df = clean_genre_name_and_id(clean_df)         # DATAFRAME GENRE TABLE
        bridge_anime_genre_df = bridge_anime_and_genre(clean_df) # DATAFRAME BRIDGE TABLE

        clean_df['timestamp'] = datetime.now().strftime('%Y-%m-%d')
        
        fact_anime_df = clean_df[[ # DATAFRAME FACT TABLE
            'anime_id', 'studio_id', 'title',
            'duration', 'episodes', 'score',
            'aired_from', 'aired_to', 'is_current',
            'validated', 'timestamp']] \
                .drop_duplicates(subset=['anime_id', 'studio_id', 'title', 'aired_to']) \
                .dropna(subset=['anime_id', 'studio_id', 'title', 'duration', 'episodes','score', 'aired_from', 'is_current', 'validated'], how='any') 
        
        dim_studio_df = clean_df[['studio_id', 'studio_name']].drop_duplicates(subset=['studio_id', 'studio_name']).dropna(how='any') # DATAFRAME STUDIO TABLE
        ##########################################

    except Exception as e:
        raise Exception(f'something unexpected went wrong: {e}')
    
    try:
        
        #load to database
        load_data_to_snoflake(dim_genre_df, dim_studio_df, fact_anime_df, bridge_anime_genre_df)
    except FileNotFoundError as fnfe:
        raise FileNotFoundError(f'could not locate the file to load data into snowflake: {fnfe}')
    except Exception as e:
        raise Exception(f'something else went wrong when wanting to load data into snowflake: {e}')

############ COMPRESSING FUNCTIONS ################
def bridge_anime_and_genre(df) -> pd.DataFrame:
    """concat the genres cilumns from 6 columns into 2 ('genre_id' & 'genre_name')"""
    try:
        return pd.DataFrame({
            'anime_id': pd.concat([df['anime_id'], df['anime_id'], df['anime_id']]), # could use melt() but this keeps consistency
            'genre_id': pd.concat([df['genre_id_1'], df['genre_id_2'], df['genre_id_3']])
        }).drop_duplicates(subset=['anime_id', 'genre_id'], keep='first').dropna(how='any')

    except Exception as e:
        raise Exception(f'issue with concating columns: {e}')

def clean_genre_name_and_id(df) -> pd.DataFrame:
    """concat the genres cilumns from 6 columns into 2 ('genre_id' & 'genre_name')"""
    try:
        return pd.DataFrame({
            'genre_id': pd.concat([df['genre_id_1'], df['genre_id_2'], df['genre_id_3']]),
            'genre_name': pd.concat([df['genre_1'], df['genre_2'], df['genre_3']])
        }).drop_duplicates(subset=['genre_id', 'genre_name'], keep='first').dropna(how='any')
    
    except Exception as e:
        raise Exception(f'issue with concating columns: {e}')
###################################################


def data_type_converter(dataframe) -> pd.DataFrame:
    """convert the datatypes for each column and convert it to the data model's datatype"""

    try:
        for column in ['episodes', 'duration', 'studio_id', 'genre_id_1', 'genre_id_2', 'genre_id_3']:
            dataframe[column] = pd.to_numeric(dataframe[column], errors='coerce').round(0).astype('Int64')

        return dataframe
    
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise e

if __name__ == '__main__':
    divide_dataframe()
