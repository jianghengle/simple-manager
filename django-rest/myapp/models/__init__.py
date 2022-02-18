from .cost import Cost
from .attachment import Attachment
from .password_reset import PasswordReset
from .my_config import MyConfig
from .vendor_subsidiary import VendorSubsidiary

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
