from celery import shared_task

from time import sleep

@shared_task
def sleep_time(time):
    sleep(time)