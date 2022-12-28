import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

User = get_user_model()


class Command(BaseCommand):
    help = "Crate a superuser, and allow password to be provided"

    def handle(self, *args, **options):
        username = "admin"
        password = "admin"

        try:
            User.objects.create_superuser(username=username, password=password)
        except IntegrityError:
            print("Base superuser already created!")
        except Exception as e:
            print("Error during superuser creation: ")
            print(e)
