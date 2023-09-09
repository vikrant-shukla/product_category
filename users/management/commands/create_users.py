# Create a file named create_users.py in your app's management/commands directory

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
import random

class Command(BaseCommand):
    help = 'Create 100 users'

    def handle(self, *args, **options):
        for i in range(1, 101):
            username = f'user{i}'
            password = 'password123'
            email = f'user{i}@example.com'
            User.objects.create_user(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'User {i} created'))
