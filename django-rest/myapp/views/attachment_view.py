from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from ..models.attachment import Attachment



@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def create_attachment(request):
    attachment = Attachment()
    attachment.from_json(request.data)
    attachment.created_by = request.user.email
    attachment.save()
    return Response(attachment.to_json())

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_attachment(request, attachment_id):
    attachment = Attachment.objects.get(pk=attachment_id)
    return Response(attachment.to_json())
