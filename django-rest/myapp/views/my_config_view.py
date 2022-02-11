from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from ..models.my_config import MyConfig


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_my_config(request):
    # Get the only one record from MyConfig table using MyConfig.get_record()
    # And return the record in json
    return Response({})


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def update_my_config(request):
    # Check if the user is super user and if not raise PermissionDenied exception
    # Get the only one record from MyConfig table MyConfig.get_record()
    # Update the config field from the request data
    # And return the record in json
    return Response({})
