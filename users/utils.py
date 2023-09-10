from django.core.mail import EmailMessage
from categories_product import settings 

def email_sending(email):
    mail_subject = "Assignment"
    mail_message = """
                    Hello,
                    Please find and go through the file attached.

                    Thanks,
                    Django Mailing System
                    """
    to_email = email 
    try:
        mail = EmailMessage(
            mail_subject,
            mail_message,
            settings.EMAIL_HOST_USER,
            to_email
            )
        mail.attach_file('media/sample.xlsx')
        mail.send()
        return "Mail Sent!!!"
    except Exception as error:
        return error