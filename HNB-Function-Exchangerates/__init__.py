import datetime
from main import run_main
import azure.functions as func
from src import logger 

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logger.info('The timer is past due!')

    try:
        run_main()
        logger.info('Python timer trigger function ran at %s', utc_timestamp)
    except Exception as e:
        logger.error(f'Error in main execution: {e}')
        raise

