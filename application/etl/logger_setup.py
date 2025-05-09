


import logging
from datetime import datetime
import watchtower


def setup_logger() -> logging.Logger:
    """Configure logging to send logs to both console and AWS CloudWatch."""
    logger = logging.getLogger('etl-pipeline')
    logger.setLevel(logging.INFO)

    # Clear existing handlers to avoid duplicates
    if logger.hasHandlers():
        logger.handlers.clear()

    # Format for logs
    formatter = logging.Formatter(
        '[%(asctime)s] - [%(levelname)s] - [%(module)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M'
    )

    # 1. Console Handler (for local/dev)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 2. CloudWatch Handler (if running in AWS)
    try:
        # Only add CloudWatch if running in AWS (e.g., Glue)
        
        cloudwatch_handler = watchtower.CloudWatchLogHandler(
            log_group_name='anime-analytics/logs/glue-job',  # Custom log group
            stream_name=f'etl-pipeline-{datetime.now().strftime("%Y-%m-%d")}'
        )

        cloudwatch_handler.setFormatter(formatter)
        logger.addHandler(cloudwatch_handler)
    except Exception as e:
        logger.error(f"Failed to set up CloudWatch logging: {e}", exc_info=True)

    # Suppress noisy loggers
    for noisy_logger in [
        'botocore.credentials',
        'botocore.auth',
        'urllib3.connectionpool',
        'snowflake.connector',
        'snowflake.connector.network',
        'snowflake.connector.connection'
    ]:
        logging.getLogger(noisy_logger).setLevel(logging.WARNING)
        logging.getLogger(noisy_logger).propagate = False

    return logger