from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
# from django.utils.crypto import get_random_string
import getpass


class Command(BaseCommand):
    help = 'Create users'

    def add_arguments(self, parser):
        parser.add_argument('-a', '--admin', action='store_true', help='Create an admin account')


    def handle(self, *args, **kwargs):
        admin = kwargs['admin']
        username = input("Enter user name: ")
        email = input("Enter Email Address: ")
        password = getpass.getpass(prompt='Enter password: ')

        if admin:
            User.objects.create_superuser(username=username, email=email, password=password)
        else:
            User.objects.create_user(username=username, email=email, password=password)