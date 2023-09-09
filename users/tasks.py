from celery import shared_task
from users.utils import email_sending

@shared_task
def send_mail_func(email):
    email_sending(email)
    
@shared_task
def send_delayed_email(email):
   email_sending(email)

