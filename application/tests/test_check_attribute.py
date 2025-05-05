
import sys
sys.path.append('../')
from mock_dataframes import clean_mock_df

from etl.check_attribute import check_attribute_length


def test_check_attribute_length(clean_mock_df):
    
    long_string = '0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789'
    df = check_attribute_length(clean_mock_df)

    assert all(df['studio_name'].str.len() <= 50)
    assert all(df['title'].str.len() <= 99)
    assert long_string not in df['title'].values

if __name__ == '__main__':
    test_check_attribute_length()
