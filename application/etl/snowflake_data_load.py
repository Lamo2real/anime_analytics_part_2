
from snowflake.connector.errors import DatabaseError, InterfaceError
from get_secrets import get_secrets_manager_values
from snowflake.connector.pandas_tools import write_pandas as wp
from sql_composite_prep import get_snowflake_connection
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
        
    except DatabaseError as dbe:
        raise dbe
    except InterfaceError as ie:
        raise ie 
    except Exception as e:
        raise e
