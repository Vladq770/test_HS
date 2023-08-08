from celery import shared_task
from time import sleep


@shared_task()
def send_code_task(number, code):
    sleep(2)
