


import logging
from datetime import datetime
import watchtower

def setup_logger() -> logging:
    """setup logging and monitoring system for AWS CloudWatch Logs"""

    date = datetime.now().strftime('%Y-%m-%d')
    log_group = 'anime-analytics/logs/glue-job' # this is set in cw_logs.tf 
    log_stream  = f'etl-pipeline-{date}'

    logger = logging.getLogger('etl-pipeline')
    logger.setLevel(logging.INFO)

    cw_handler = watchtower.CloudWatchLogHandler(log_group=log_group, stream_name=log_stream)
    formatter = logging.Formatter(
        '[%(asctime)s] - [%(levelname)s] - [%(module)s]: %(message)s',
        datefmt='%Y-%m-%d_%H-%M-%S'
        )
    cw_handler.setFormatter(formatter)
    logger.addHandler(cw_handler)

    return logger

    # date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    # logging.basicConfig(
    #     filename=f"etl-pipeline-{date}.log",
    #     filemode='a',
    #     format='[%(asctime)s] - [%(levelname)s] - [%(module)s]: %(message)s',
    #     level=logging.INFO,
    #     datefmt='%Y-%m-%d %H:%M'
    # )


    # for noisy_logger in [
    #     'botocore.credentials',
    #     'botocore.auth',
    #     'urllib3.connectionpool',
    #     'snowflake.connector', 
    #     'snowflake.connector.network',
    #     'snowflake.connector.connection'
    #     ]:
    #     logger = logging.getLogger(noisy_logger)
    #     logger.setLevel(logging.WARNING)
    #     logger.propagate = False
    
    # return logging.getLogger('etl-pipeline')