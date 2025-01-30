import signal
import sys
import logging
import time
from services.scheduler import Scheduler


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = Scheduler()

def graceful_shutdown(_, __):
    logger.info("Graceful shutdown initiated...")
    scheduler.stop_schedule()
    sys.exit(0)

if __name__ == "__main__":
    try:
        logger.info("Starting cronjob scheduler...")

        signal.signal(signal.SIGINT, graceful_shutdown)
        signal.signal(signal.SIGTERM, graceful_shutdown)

        scheduler.start_scheduler()
        logger.info("Cronjob started successfully.")
        
        while True:
            time.sleep(1)

    except Exception as e:
        logger.error(f"Failed to start the cronjob: {e}")
        sys.exit(1)
