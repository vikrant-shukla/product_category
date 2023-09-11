from celery import shared_task
from users.utils import email_sending

@shared_task
def send_mail_func(email):
    """Task to send mail to emails with excel file"""
    email_sending(email)
    
@shared_task
def send_delayed_email(email):
   """Task to send mail to emails with excel file after 2 mins of api call"""
   email_sending(email)

