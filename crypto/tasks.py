from celery import shared_task


@shared_task
def check_certificates():
    pass
    # call_command('certificates', '--all')
