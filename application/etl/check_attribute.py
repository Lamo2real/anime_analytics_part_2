

import pandas as pd
import logging
from logger_setup import setup_logger
setup_logger()

logger = logging.getLogger(__name__)

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
        cleaned_df = cleaned_df[~condition]    #the '~' will make sure to keep the records that followes the requirements but reversed
        return cleaned_df
    
    except KeyError as e:
        logger.error(f"Missing expected column: {e}", exc_info=True)
        raise
    except Exception as e:
        logger.critical(f'unexpected error: {e}', exc_info=True)
        raise 