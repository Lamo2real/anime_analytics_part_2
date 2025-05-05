

import pytest
import pandas as pd

@pytest.fixture
def raw_mock_df():
    """
    this is the mock dta for testing the 'data_type_converter' function
    to check if the datatypes are converted, and is used in 'test_data_type_converter'.
    """ 
    return pd.DataFrame({
        'anime_id': [3, 4, 676],
        'title': ['naruto', 'baki', 'demon slayer'],
        'aired_from': ['2002-10-03', '2001-01-08', '2019-04-06'],
        'aired_to': ['2007-02-08', '2001-06-25', '2019-09-28'],
        'episodes': [220.0, 24.0, 26.0],
        'duration': [23.0, 25.0, 23.0],
        'studio_name': ['Pierrot', 'Group TAC', 'ufotable'],
        'studio_id': [3.0, 7.0, 20.0],
        'genre_1': ['Action', 'Action', 'Action'],
        'genre_2': ['Adventure', 'Martial Arts', 'Supernatural'],
        'genre_3': ['Shounen', 'Sports', 'Demons'],
        'genre_id_1': [1.0, 1.0, 1.0],
        'genre_id_2': [2.0, 9.0, 12.0],
        'genre_id_3': [15.0, 17.0, 30.0],
        'score': [7.9, 7.4, 8.7],
        'validated': [True, True, True]
    })

@pytest.fixture
def clean_mock_df():
    """
    this mock dataset is used for 'test_check_attribute_length' 
    to test the logic of 'check_attribute_length' function 
    """
    long_string = '0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789'
    return pd.DataFrame({
        'anime_id': [3, 4, 676],
        'title': ['naruto', long_string, 'demon slayer'],
        'aired_from': ['2002-10-03', '2001-01-08', '2019-04-06'],
        'aired_to': ['2007-02-08', '2001-06-25', '2019-09-28'],
        'episodes': [220, 24, 26],
        'duration': [23, 25, 23],
        'studio_name': ['Pierrot', 'Group TAC', long_string],
        'studio_id': [3, 7, 20],
        'genre_1': ['Action', 'Action', 'Action'],
        'genre_2': ['Adventure', 'Martial Arts', 'Supernatural'],
        'genre_3': ['Shounen', 'Sports', 'Demons'],
        'genre_id_1': [1, 1, 1],
        'genre_id_2': [2, 9, 12],
        'genre_id_3': [15, 17, 30],
        'score': [7.9, 7.4, 8.7],
        'validated': [True, True, True]
    })
    

@pytest.fixture
def managed_mock_df():
    """
    this is used in 'test_clean_genre_name_and_id' & 'test_bridge_anime_and_genre'
    to test 2 function: 'clean_genre_name_and_id' & 'bridge_anime_and_genre'
    """

    return pd.DataFrame({
        'anime_id': [3, 4, 676],
        'title': ['naruto', 'long_string', 'demon slayer'],
        'aired_from': ['2002-10-03', '2001-01-08', '2019-04-06'],
        'aired_to': ['2007-02-08', None, '2019-09-28'],
        'episodes': [220, 24, 26],
        'duration': [23, 25, 23],
        'is_current': [True, False, True],
        'studio_name': [None, 'Group TAC', 'long_string'],
        'studio_id': [3, 7, 20],
        'genre_1': ['Action', None, 'Action'],
        'genre_2': ['Adventure', 'Martial Arts', 'Supernatural'],
        'genre_3': ['Shounen', 'Sports', 'Demons'],
        'genre_id_1': [1, 1, 1],
        'genre_id_2': [2, 9, 12],
        'genre_id_3': [15, 17, 30],
        'score': [7.9, 7.4, None],
        'validated': [True, True, True]
    })


