import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
User = get_user_model()

mysu = os.environ.get('MY_SUPERUSER')
mysupwd = os.environ.get('MY_SUPERUSER_PASSWORD')

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username=mysu).exists():
            User.objects.create_superuser(mysu, mysu, mysupwd)
