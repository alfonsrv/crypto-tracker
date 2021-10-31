from celery import shared_task

from crypto.services import crypto_update


@shared_task
def crypto_update_task():
    crypto_update()
