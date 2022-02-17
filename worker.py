from celery import Celery
from celery.utils.log import get_task_logger
from celery.schedules import crontab

import os
import time
from dotenv import load_dotenv


# logger = get_task_logger(__name__)

load_dotenv(".env")

celery = Celery(__name__)
celery.conf.update(
    result_expires=60,
    task_acks_late=True,
    broker_url=os.environ.get("CELERY_BROKER_URL"),
    result_backend=os.environ.get("CELERY_RESULT_BACKEND")
)

__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=5, minute=30, day_of_week=1),
        cleanup_logs.s(),
    )


@celery.task
def cleanup_logs():
    try:
        file_path = os.path.join(__location__, f"gps_reports.log")
        with open(file_path, "w"): pass
        # logger.info(f"Log file has been cleaned!")
    except:
        # logger.warning(f"Exception happened while cleaning logs file")
        pass


@celery.task(name="test_task")
def test_task(a, b, c):
    result = a / b
    # logger.info(f'Result is: {result}')
    time.sleep(c)

    return result