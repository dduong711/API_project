from celery.decorators import task
from celery.utils.log import get_task_logger

from .emails import mongodb_notification_email

logger = get_task_logger(__name__)

@task(name='action_notification_email')
def notify(context):
    mongodb_notification_email.send_mail(context)
    return('Task Done')
