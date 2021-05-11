from django.dispatch import Signal, receiver 
from django.core.mail import send_mail
from the_techbox import settings
from django.core.mail import EmailMessage

notification = Signal(providing_args=['items'])

@receiver(notification)
def show_notification(sender,**kwargs):
    dic = kwargs['items']
    subject = 'Mail to Admin'
    message = dic + ' item has been added in TechBox' 
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['deepaktumdiya.thoughtwin@gmail.com']
    email = EmailMessage(subject, message, email_from, recipient_list)
    email.send(fail_silently=False)
    return None
