
import pandas as pd 
import logging
from logger_setup import setup_logger
setup_logger()

logger = logging.getLogger(__name__)

############ COMPRESSING FUNCTIONS ################
def bridge_anime_and_genre(df) -> pd.DataFrame:
    """concat the genres cilumns from 6 columns into 2 ('genre_id' & 'genre_name')"""
    try:
        return pd.DataFrame({
            'anime_id': pd.concat([df['anime_id'], df['anime_id'], df['anime_id']]), # could use melt() but this keeps consistency
            'genre_id': pd.concat([df['genre_id_1'], df['genre_id_2'], df['genre_id_3']])
        }).drop_duplicates(subset=['anime_id', 'genre_id'], keep='first').dropna(how='any')
    
    except KeyError as e:
        logger.error(f"Missing expected column: {e}", exc_info=True)
        raise
    except (TypeError, AttributeError, ValueError) as e:
        logger.error(f"Data formatting error during genre DataFrame creation: {e}", exc_info=True)
        raise
    except Exception as e:
        logger.critical(f'issue with concating columns: {e}', exc_info=True)
        raise

def clean_genre_name_and_id(df) -> pd.DataFrame:
    """concat the genres cilumns from 6 columns into 2 ('genre_id' & 'genre_name')"""
    try:
        return pd.DataFrame({
            'genre_id': pd.concat([df['genre_id_1'], df['genre_id_2'], df['genre_id_3']]),
            'genre_name': pd.concat([df['genre_1'], df['genre_2'], df['genre_3']])
        }).drop_duplicates(subset=['genre_id', 'genre_name'], keep='first').dropna(how='any')
    
    except KeyError as ke:
        logger.error(f"Missing expected column: {ke}", exc_info=True)
        raise
    except (TypeError, AttributeError, ValueError) as e:
        logger.error(f"Data formatting error during genre DataFrame creation: {e}", exc_info=True)
        raise
    except Exception as e:
        logger.critical(f"Unexpected issue with genre DataFrame creation: {e}", exc_info=True)
        raise
    
def clean_null_and_duplicates(managed_df) -> pd.DataFrame:
    """
    drop all records that has duplicate combination of
    values in the dataframe and drop Null values
    """
    try:
        no_duplicate_df = managed_df[
                [ # DATAFRAME FACT TABLE
                    'anime_id', 'studio_id', 'title',
                    'duration', 'episodes', 'score',
                    'aired_from', 'aired_to', 'is_current',
                    'validated', 'timestamp_loaded'
                ]
            ] \
            .drop_duplicates(subset=['anime_id', 'studio_id', 'title', 'aired_to']) \
            .dropna(subset=[
                'anime_id', 'studio_id', 'title',
                'duration', 'episodes','score',
                'aired_from', 'is_current', 'validated'
            ], how='any')
        return no_duplicate_df
    
    except KeyError as ke:
        logger.error(f"Missing expected column: {ke}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f'unexpected error: {e}', exc_info=True)
        raise
    
def clean_dim_studio_df(df):

    try:
        clean_df = df[
            ['studio_id', 'studio_name']
            ].drop_duplicates(subset=['studio_id', 'studio_name']).dropna(how='any')
        return clean_df
    
    except KeyError as ke:
        logger.error(f"Missing expected column: {ke}", exc_info=True)
        raise    
    except Exception as e:
        logger.critical(f'unexpected error: {e}', exc_info=True)
        raise

###################################################


def data_type_converter(dataframe) -> pd.DataFrame:
    """convert the datatypes for each column and convert it to the data model's datatype"""

    try:
        for column in ['episodes', 'duration', 'studio_id', 'genre_id_1', 'genre_id_2', 'genre_id_3']:
            dataframe[column] = pd.to_numeric(dataframe[column], errors='coerce').round(0).astype('Int64')

        return dataframe
    
    except ValueError as ve:
        logger.critical(f'{ve}', exc_info=True)
        raise 
    except Exception as e:
        logger.critical(f'unexpected error: {e}', exc_info=True)
        raise
