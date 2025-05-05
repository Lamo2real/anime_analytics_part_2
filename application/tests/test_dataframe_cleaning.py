
import pandas as pd
import sys
from datetime import datetime
sys.path.append('../')
from etl.dataframe_cleaning import data_type_converter, bridge_anime_and_genre, clean_genre_name_and_id, clean_null_and_duplicates, clean_dim_studio_df
from mock_dataframes import raw_mock_df, managed_mock_df 


def test_data_type_converter(raw_mock_df):

    df = data_type_converter(raw_mock_df)
    assert isinstance(df, pd.DataFrame)
    for col in ['episodes', 'duration', 'studio_id', 'genre_id_1', 'genre_id_2', 'genre_id_3']:
        assert df[col].map(type).eq(int).all()


def test_clean_genre_name_and_id(managed_mock_df):

    refined_df = clean_genre_name_and_id(managed_mock_df)
    assert type(refined_df) == pd.DataFrame
    assert 'genre_id_1' not in refined_df.columns
    assert 'genre_id' in refined_df.columns
    assert not refined_df['genre_id'].isna().any()
    assert not refined_df[['genre_id', 'genre_name']].duplicated().any()




def test_bridge_anime_and_genre(managed_mock_df):
    
    refined_df = bridge_anime_and_genre(managed_mock_df)
    assert type(refined_df) == pd.DataFrame
    assert 'genre_id_1' not in refined_df.columns
    assert 'genre_id' in refined_df.columns
    assert not refined_df['genre_id'].isna().any()
    assert not refined_df[['anime_id', 'genre_id']].duplicated().any()

def test_clean_null_and_duplicates(managed_mock_df):
    """test the 'clean_null_and_duplicates' """

    managed_mock_df['timestamp_loaded'] = datetime.now().strftime('%Y-%m-%d')
    refined_df = clean_null_and_duplicates(managed_mock_df)

    assert not refined_df[
        [
            'anime_id', 'studio_id', 'title',
            'duration', 'episodes', 'score',
            'aired_from', 'aired_to', 'is_current',
            'validated', 'timestamp_loaded'
        ]
        ].duplicated().any()
    
    assert not refined_df[
        [
            'anime_id', 'studio_id', 'title',
            'duration', 'episodes','score',
            'aired_from', 'is_current', 'validated'
        ]
        ].isna().any().any()
    
def test_clean_dim_studio_df(managed_mock_df):

    df = clean_dim_studio_df(managed_mock_df)
    assert not df[['studio_id', 'studio_name']].isna().any().any()
    assert not df[['studio_id', 'studio_name']].duplicated().any()

    

if __name__ == '__main__':
    test_clean_genre_name_and_id()
