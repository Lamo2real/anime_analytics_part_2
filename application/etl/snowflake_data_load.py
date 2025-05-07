
from get_secrets import get_secrets_manager_values
from snowflake.connector.pandas_tools import write_pandas as wp
from sql_composite_prep import get_snowflake_connection
import logging
from logger_setup import setup_logger
setup_logger()

logger = logging.getLogger(__name__)

def load_data_to_snoflake(genre_df, studio_df, anime_df, bridge_df):
    """
    use aws secrets manager secrets, fecth the secrets
    and use them as credentials when 
    COPYing csv into snowflake's database correlating table in bulk.
    """
    
    try:
        secrets = get_secrets_manager_values()
        
        if None in secrets.values():
            missing_keys = [key for key, value in secrets.items() if value is None]
            logger.critical(f'missing values for keys: {missing_keys}')
            
        snowpy_con = get_snowflake_connection()
        all_dataframes = [
                (genre_df, 'DIM_GENRE'),
                (studio_df, 'DIM_STUDIO'),
                (anime_df, 'FACT_ANIME'),
                (bridge_df, 'BRIDGE_ANIME_GENRE')
        ]

        for df, db_table in all_dataframes:
            df = df.reset_index(drop=True)
            wp(snowpy_con, df, table_name=db_table)
        
    except KeyError as ke:
        logger.error(f'could not find values in secrets manager: {ke}', exc_info=True)
        raise
    except Exception as e:
        logger.critical(f'unexpected error: {e}', exc_info=True)
        raise
