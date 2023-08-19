import time

from celery import shared_task


@shared_task
def test() -> bool:
    time.sleep(5)
    print('Start test task')
    return True