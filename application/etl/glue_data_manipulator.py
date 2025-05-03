import pandas as pd 
from datetime import datetime
from extract_data_s3 import s3_data_extract
from snowflake_data_load import load_data_to_snoflake
from check_attribute import check_attribute_length
from sql_composite_prep import queries, get_snowflake_connection, create_composite_key, filter_new_rows
from dataframe_cleaning import bridge_anime_and_genre, clean_genre_name_and_id, data_type_converter



def divide_dataframe():
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

        fact_anime_df = managed_df[[ # DATAFRAME FACT TABLE
            'anime_id', 'studio_id', 'title',
            'duration', 'episodes', 'score',
            'aired_from', 'aired_to', 'is_current',
            'validated', 'timestamp_loaded']] \
                .drop_duplicates(subset=['anime_id', 'studio_id', 'title', 'aired_to']) \
                .dropna(subset=['anime_id', 'studio_id', 'title', 'duration', 'episodes','score', 'aired_from', 'is_current', 'validated'], how='any') 

        dim_studio_df = managed_df[['studio_id', 'studio_name']].drop_duplicates(subset=['studio_id', 'studio_name']).dropna(how='any') # DATAFRAME STUDIO TABLE
        ##########################################

        for each_df in [dim_genre_df, bridge_anime_genre_df, fact_anime_df, dim_studio_df]:
            each_df.columns = [col.upper() for col in each_df.columns]

    except Exception as e:
        raise Exception(f'something unexpected went wrong: {e}')

    try:
        ##### CONNECT TO SNOWFLAKE #####
        snowpy_con = get_snowflake_connection()

        ##### DATABASE QUERIES #####
        query = queries() #this  has all queries stored as a dictionary

        existing_dim_genre_df = pd.read_sql(query['dim_genre_query'], snowpy_con)
        existing_dim_studio_df = pd.read_sql(query['dim_studio_query'], snowpy_con)
        existing_fact_df = pd.read_sql(query['fact_anime_query'], snowpy_con)
        existing_bridge_df = pd.read_sql(query['bridge_query'], snowpy_con)

        ##### CREATING COMPOSITE KEYS #####

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
        ###################################

        ####### FILTER AND REMOVE EQUIVALENT COMPOSITE KEYS #######
        filtered_dim_genre_df = filter_new_rows(dim_genre_df, existing_dim_genre_df)
        filtered_dim_studio_df = filter_new_rows(dim_studio_df, existing_dim_studio_df)
        filtered_fact_df = filter_new_rows(fact_anime_df, existing_fact_df)
        filtered_bridge_df = filter_new_rows(bridge_anime_genre_df, existing_bridge_df)
        ###########################################################

        #load to database
        load_data_to_snoflake(filtered_dim_genre_df, filtered_dim_studio_df, filtered_fact_df, filtered_bridge_df)
    except FileNotFoundError as fnfe:
        raise FileNotFoundError(f'could not locate the file to load data into snowflake: {fnfe}')
    except Exception as e:
        raise Exception(f'something else went wrong when wanting to load data into snowflake: {e}')



if __name__ == '__main__':
    divide_dataframe()

