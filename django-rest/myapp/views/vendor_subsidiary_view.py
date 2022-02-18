from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..models.vendor_subsidiary import VendorSubsidiary

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_vendor_subsidiaries(request):
    vendor_subsidiaries = VendorSubsidiary.objects.all()
    return Response([i.to_json() for i in vendor_subsidiaries])
