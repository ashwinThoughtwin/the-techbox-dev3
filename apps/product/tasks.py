from celery import shared_task
from django.core.mail import send_mail
from time import sleep
from the_techbox import settings
from django.core.mail import EmailMessage

@shared_task
def send_emails(emails,borrow):
    subject = 'Requesting for '+ borrow
    message = 'Hi Your Request for '+ borrow + ' is received' 
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [emails]
    email = EmailMessage(subject, message, email_from, recipient_list)
    email.send(fail_silently=False)
    return None
