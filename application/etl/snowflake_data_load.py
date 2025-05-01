
import pandas as pd
import snowflake.connector
from snowflake.connector.error import DatabaseError, InterfaceError
from get_secrets import get_secrets_manager_values
from snoflake.connector.pandas_tools import write_pandas as wp

def load_data_to_snoflake(genre_df, studio_df, anime_df, bridge_df):
    """
    use aws secrets manager secrets, fecth the secrets
    and use them as credentials when 
    COPYing csv into snowflake's database correlating table in bulk.
    """
    
    try:
        secrets = get_secrets_manager_values()
        
        if None in secrets.values():
            raise KeyError
        snowpy_con = snowflake.connector.connect(
                user      = secrets['USER'],
                password  = secrets['PASSWORD'],
                account   = secrets['ACCOUNT'],
                role      = secrets['ROLE'],
                warehouse = 'anime_analytics_wh',
                database  = 'anime_analytics_db',
                schema    = 'analytics'
                )
        
        all_dataframes = [
                (genre_df, 'dim_genre'),
                (studio_df, 'dim_studio'),
                (anime_df, 'fact_anime'),
                (bridge_df, 'bridge_genre_anime')
        ]

        for df, db_table in all_dataframes:
            wp(snowpy_con, df, table_name=db_table)
        
    except DatabaseError as dbe:
        raise dbe
    except InterfaceError as ie:
        raise ie 
    except Exception as e:
        raise e
