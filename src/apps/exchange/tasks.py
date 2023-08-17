import time

from celery import shared_task


@shared_task
def test() -> bool:
    time.sleep(3)
    return True