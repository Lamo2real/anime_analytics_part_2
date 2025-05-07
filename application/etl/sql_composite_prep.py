from snowflake.connector.errors import DatabaseError, InterfaceError
from snowflake.connector.connection import SnowflakeConnection
from get_secrets import get_secrets_manager_values
import snowflake.connector
import pandas as pd
import logging
from logger_setup import setup_logger
setup_logger()

logger = logging.getLogger(__name__)

def queries() -> dict:
    """return all quewries needed for read_sql"""
    return {
        'dim_genre_query': 'SELECT GENRE_ID, GENRE_NAME FROM DIM_GENRE',
        'dim_studio_query': 'SELECT STUDIO_ID, STUDIO_NAME FROM DIM_STUDIO',
        'fact_anime_query': 'SELECT ANIME_ID, EPISODES, SCORE FROM FACT_ANIME',
        'bridge_query': 'SELECT ANIME_ID, GENRE_ID FROM BRIDGE_ANIME_GENRE'
    }

def create_composite_key(df, columns) -> pd.DataFrame:
    """take dataframe of the table and create a composite key with the array of columns"""
    df['COMPOSITE_KEY'] = df[columns].astype(str).agg('_'.join, axis=1)
    return df 

def filter_new_rows(new_df, existing_df) -> pd.DataFrame:
    """
    return the records that are NOT (thanks to ~) in existing_df.
    this means that if the new dataframe has the same composite key
    in the database already as in the new upcoming dataframe from the datalake,
    then dont return that record in the dataframe.
    Only return the dataframes/records that does NOT match the existing dataframe. 
    """
    return new_df[~new_df['COMPOSITE_KEY'].isin(existing_df['COMPOSITE_KEY'])].drop(columns=['COMPOSITE_KEY'])

def get_snowflake_connection() -> SnowflakeConnection:
    """
    take the AWS Secrets Manager secrets and use them to
    get access to Snowflake database.
    """
    try:
        secrets = get_secrets_manager_values()

        if None in secrets.values():
            missing_keys = [key for key, value in secrets.items() if value is None]
            logger.critical(f'missing values for keys: {missing_keys}')

        return snowflake.connector.connect(
                user      = secrets['USER'],
                password  = secrets['PASSWORD'],
                account   = secrets['ACCOUNT'],
                role      = secrets['ROLE'],
                warehouse = 'ANIME_ANALYTICS_WH',
                database  = 'ANIME_ANALYTICS_DB',
                schema    = 'ANALYTICS'
            )
    except DatabaseError as de:
        logger.error(f'database error: {de}', exc_info=True)
        raise
    except InterfaceError as ie:
        logger.error(f'database connection error: {ie}', exc_info=True)
        raise
    except FileNotFoundError as fnfe:
        logger.critical(f'could not find file error: {fnfe}', exc_info=True)
        raise 
    except Exception as e:
        logger.critical(f'unexpected error: {e}', exc_info=True)
        raise 