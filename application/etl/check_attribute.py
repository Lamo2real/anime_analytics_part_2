

import pandas as pd

def check_attribute_length(cleaned_df) -> pd.DataFrame:
    """
    Claen the data inside and limit them into according data limits set
    by CRUD durring database migration script
    """

    try:
        cleaned_df = cleaned_df.astype({
            'studio_name': 'string',
            'title': 'string'
        })

        condition = (cleaned_df['studio_name'].str.len() > 50) | (cleaned_df['title'].str.len() > 99)
        cleaned_df = cleaned_df[~condition]    #the '~' will make sure to keep the rows that followes the requirements

        return cleaned_df
            
    except Exception as e:
        raise e