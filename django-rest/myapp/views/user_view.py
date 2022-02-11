import uuid
from datetime import datetime, timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
User = get_user_model()
from ..models.password_reset import PasswordReset
from ..services.ses_service import send_email
from django.conf import settings

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_all_emails(request):
    users = User.objects.all()
    emails = []
    invoice_receiver = settings.INVOICE_RECEIVER_EMAIL
    for u in users:
        if u.is_active and u.email != invoice_receiver:
            emails.append(u.email)
    return Response(emails)

@api_view(['POST'])
def create_password_reset(request):
    email = request.data['email']
    user = User.objects.get(email=email)
    password_reset = PasswordReset()
    password_reset.email = email
    password_reset.key = str(uuid.uuid4())
    password_reset.save()
    send_password_reset_email(password_reset)
    return Response()

def send_password_reset_email(password_reset):
    webapp = settings.WEB_APP_DOMAIN
    password_reset_link = webapp + '/change-password/' + password_reset.key
    body_text = EMAIL_BODY_TEXT.format(password_reset_link)
    body_html = EMAIL_BODY_HTML.format(password_reset_link, password_reset_link)
    recipents = [password_reset.email]
    send_email(recipents, EMAIL_SUBJECT, body_text, body_html)

@api_view(['GET'])
def get_password_reset_by_key(request, key):
    password_reset = PasswordReset.objects.get(key=key)
    now = datetime.now(timezone.utc)
    if (now - password_reset.created_at).total_seconds() > 3600:
        password_reset.delete()
        raise PermissionDenied({'message': 'The link has expired.'})
    return Response(password_reset.to_json())

@api_view(['POST'])
def change_password(request, key):
    password_reset = PasswordReset.objects.get(key=key)
    now = datetime.now(timezone.utc)
    if (now - password_reset.created_at).total_seconds() > 3600:
        password_reset.delete()
        raise PermissionDenied({'message': 'The link has expired.'})
    password = request.data['password']
    user = User.objects.get(email=password_reset.email)
    user.set_password(password)
    user.save()
    password_reset.delete()
    return Response()


EMAIL_SUBJECT = "Simple Manager Password Reset"

EMAIL_BODY_TEXT = "Please use the following link to change your password:\r\n{}"

EMAIL_BODY_HTML = """<html>
<body>
  <p>Please use the following link to change your password:</p>
  <p><a href='{}' target="_blank">{}</a></p>
</body>
</html>
"""