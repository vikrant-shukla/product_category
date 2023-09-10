# Create a file named create_users.py in your app's management/commands directory

import string
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
import random

class Command(BaseCommand):
    help = 'Create 100 users'

    def handle(self, *args, **options):
        

        for i in range(1, 101):
            username = f'user{i}'
            first_name = f"firstName{i}"
            last_name = f"lastName{i}"
            password = 'password123'
            email = f'user{i}@example.com'
            User.objects.create_user(username=username,first_name=first_name, last_name=last_name, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'User {i} created'))
