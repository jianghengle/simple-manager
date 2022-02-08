import os, random, string
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from ..services.s3_service import create_presigned_post, create_presigned_url
from django.conf import settings


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_upload_url(request):
    filename = request.data['filename']
    name, ext = os.path.splitext(filename)
    stage = os.environ.get('STAGE', 'development')
    key = stage + '/attachments/' + name + '.' + get_random_string(16) + ext
    url = create_presigned_post(settings.S3_BUCKET, key)
    url['bucket'] = settings.S3_BUCKET
    url['key'] = key
    return Response(url)

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_download_url(request):
    bucket = request.data['bucket']
    key = request.data['key']
    url = create_presigned_url(bucket, key)
    return Response({'url': url})

def get_random_string(n):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))
