

import pandas as pd 
import warnings
from datetime import datetime
from extract_data_s3 import s3_data_extract
from snowflake_data_load import load_data_to_snoflake
from check_attribute import check_attribute_length
from sql_composite_prep import queries, get_snowflake_connection, create_composite_key, filter_new_rows
from dataframe_cleaning import bridge_anime_and_genre, clean_genre_name_and_id, data_type_converter, clean_null_and_duplicates, clean_dim_studio_df
import logging
from logger_setup import setup_logger
setup_logger()

logger = logging.getLogger(__name__)


def main():
    """create three dataframes of the one big table from S3 data lake"""

    try:
        raw_df = s3_data_extract() # extract data 

        ######### TRANSFORM DATA ##############
        clean_df = data_type_converter(raw_df)
        managed_df = check_attribute_length(clean_df)
        managed_df.insert(loc=7, column='is_current', value=managed_df['aired_to'].isna()) 
        dim_genre_df = clean_genre_name_and_id(managed_df)         # DATAFRAME GENRE TABLE
        bridge_anime_genre_df = bridge_anime_and_genre(managed_df) # DATAFRAME BRIDGE TABLE

        managed_df['timestamp_loaded'] = datetime.now().strftime('%Y-%m-%d')

        fact_anime_df = clean_null_and_duplicates(managed_df)
        dim_studio_df = clean_dim_studio_df(managed_df) # DATAFRAME STUDIO TABLE
        ##########################################

        for each_df in [dim_genre_df, bridge_anime_genre_df, fact_anime_df, dim_studio_df]:
            each_df.columns = [col.upper() for col in each_df.columns]

    except FileNotFoundError as fnfe:
        logger.error(f'could not find file: {e}', exc_info=True)
        raise
    except Exception as e:
        logger.critical(f'unexpected error: {e}', exc_info=True)
        raise


    try:
        ##### CONNECT TO SNOWFLAKE #####
        snowpy_con = get_snowflake_connection()

        ##### DATABASE QUERIES #####
        query = queries() #this  has all queries stored as a dictionary
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)

            existing_dim_genre_df = pd.read_sql(query['dim_genre_query'], snowpy_con)
            existing_dim_studio_df = pd.read_sql(query['dim_studio_query'], snowpy_con)
            existing_fact_df = pd.read_sql(query['fact_anime_query'], snowpy_con)
            existing_bridge_df = pd.read_sql(query['bridge_query'], snowpy_con)

        ################# CREATING COMPOSITE KEYS #################
        # ---- DIM GENRE TABLE ---- #
        existing_dim_genre_df = create_composite_key(existing_dim_genre_df, ['GENRE_ID', 'GENRE_NAME'])
        dim_genre_df = create_composite_key(dim_genre_df, ['GENRE_ID', 'GENRE_NAME'])
        # ------------------------- #

        # ---- DIM STUDIO TABLE --- #
        existing_dim_studio_df = create_composite_key(existing_dim_studio_df, ['STUDIO_ID', 'STUDIO_NAME'])
        dim_studio_df = create_composite_key(dim_studio_df, ['STUDIO_ID', 'STUDIO_NAME'])
        # ------------------------- #

        # ------- FACT TABLE ------ #
        existing_fact_df = create_composite_key(existing_fact_df, ['ANIME_ID', 'EPISODES', 'SCORE'])
        fact_anime_df = create_composite_key(fact_anime_df, ['ANIME_ID', 'EPISODES', 'SCORE'])
        # ------------------------- #

        # ------- BRIDGE TABLE----- #
        existing_bridge_df = create_composite_key(existing_bridge_df, ['ANIME_ID', 'GENRE_ID'])
        bridge_anime_genre_df = create_composite_key(bridge_anime_genre_df, ['ANIME_ID', 'GENRE_ID'])
        # ------------------------- #
        ###########################################################

        ####### FILTER AND REMOVE EQUIVALENT COMPOSITE KEYS #######
        filtered_dim_genre_df = filter_new_rows(dim_genre_df, existing_dim_genre_df)
        filtered_dim_studio_df = filter_new_rows(dim_studio_df, existing_dim_studio_df)
        filtered_fact_df = filter_new_rows(fact_anime_df, existing_fact_df)
        filtered_bridge_df = filter_new_rows(bridge_anime_genre_df, existing_bridge_df)
        ###########################################################

        ################### LOAD TO DATABSE #######################
        load_data_to_snoflake(filtered_dim_genre_df, filtered_dim_studio_df, filtered_fact_df, filtered_bridge_df)
        ###########################################################

    except FileNotFoundError as fnfe:
        logger.error(f'could not locate the file to load data into snowflake: {fnfe}', exc_info=True)
        raise
    except Exception as e:
        logger.critical(f'something else went wrong when wanting to load data into snowflake: {e}', exc_info=True)
        raise



if __name__ == '__main__':
    main()

