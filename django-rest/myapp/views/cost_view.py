from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from ..models.cost import Cost
from django.db.models import Q
from ..services.ses_service import send_email
from ..services.approve_service import add_waterprints
from django.conf import settings

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_costs(request):
    filter_option = request.GET.get('filterOption')
    if filter_option == 'working':
        email = request.user.email
        costs = Cost.objects.filter(status='Open').filter(Q(created_by=email) | Q(reviewers__icontains=email))
    else:
        costs = Cost.objects.all()
    return Response([c.to_json() for c in costs])

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_cost(request, cost_id):
    cost = Cost.objects.get(pk=cost_id)
    return Response(cost.to_json())

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def create_cost(request):
    cost = Cost()
    cost.from_json(request.data)
    cost.save()
    if (request.data['sendEmail']):
        send_notification(request.user.email, cost)
    return Response(cost.to_json())

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def update_cost(request, cost_id):
    cost = Cost.objects.get(pk=cost_id)
    check_edit(request.user.email, cost)
    if cost.status != request.data['status']:
        check_close(request.user.email, cost)
    cost.from_json(request.data)
    cost.save()
    if request.data['status'] == 'Approved':
        add_waterprints(cost)
        send_approval(request.user.email, cost)
    if request.data['status'] == 'Rejected':
        send_rejection(request.user.email, cost)
    return Response(cost.to_json())

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def delete_cost(request, cost_id):
    cost = Cost.objects.get(pk=cost_id)
    check_edit(request.user.email, cost)
    cost.delete()
    return Response()

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def send_email_for_cost(request, cost_id):
    cost = Cost.objects.get(pk=cost_id)
    if cost.status != 'Open':
        raise PermissionDenied({'message': 'Status does not allow to send email.'})
    send_notification(request.user.email, cost)
    return Response()

def check_edit(email, cost):
    if cost.status != 'Open':
        raise PermissionDenied({'message': 'Status does not allow to edit.'})
    if email == cost.created_by:
        return
    if email in cost.reviewers:
        return
    raise PermissionDenied({'message': 'You do not have permission to edit.'})

def check_close(email, cost):
    if cost.status != 'Open':
        raise PermissionDenied({'message': 'Status does not allow to close.'})
    if email in cost.reviewers:
        return
    raise PermissionDenied({'message': 'You do not have permission to close.'})

def send_notification(email, cost):
    subject = 'Open: ' + EMAIL_SUBJECT.format(cost.id, cost.subject)
    webapp = settings.WEB_APP_DOMAIN
    invoice_link = webapp + '/invoice/' + str(cost.id)
    first_sentense = 'On behalf of User {}, Vanityart Invoice System sent this notification regarding Invoice({}): {}.'.format(email, cost.id, cost.subject)
    body_text = EMAIL_BODY_TEXT.format(first_sentense, webapp, cost.id, invoice_link)
    body_html = EMAIL_BODY_HTML.format(first_sentense, webapp, cost.id, invoice_link)
    recipents = get_recipents(email, cost)
    send_email(recipents, subject, body_text, body_html)

def get_recipents(email, cost):
    recipents = [email]
    if cost.created_by:
        recipents.append(cost.created_by)
    if cost.reviewers:
        recipents = recipents + cost.reviewers.split(',')
    recipents = list(set(recipents))
    if 'invoice@vanityart.com' in recipents:
        recipents.remove('invoice@vanityart.com')
    return recipents

def send_approval(email, cost):
    subject = 'Approved: ' + EMAIL_SUBJECT.format(cost.id, cost.subject)
    webapp = settings.WEB_APP_DOMAIN
    invoice_link = webapp + '/invoice/' + str(cost.id)
    first_sentense = 'User {} has approved this Invoice({}): {}.'.format(email, cost.id, cost.subject)
    body_text = EMAIL_BODY_TEXT.format(first_sentense, webapp, cost.id, invoice_link)
    body_html = EMAIL_BODY_HTML.format(first_sentense, webapp, cost.id, invoice_link)
    recipents = get_recipents(email, cost)
    recipents = list(set(recipents + settings.INVOICE_APPROVAL_RECIPENTS.split(',')))
    send_email(recipents, subject, body_text, body_html)

def send_rejection(email, cost):
    subject = 'Rejected: ' + EMAIL_SUBJECT.format(cost.id, cost.subject)
    webapp = settings.WEB_APP_DOMAIN
    invoice_link = webapp + '/invoice/' + str(cost.id)
    first_sentense = 'User {} has rejected this Invoice({}): {}.'.format(email, cost.id, cost.subject)
    body_text = EMAIL_BODY_TEXT.format(first_sentense, webapp, cost.id, invoice_link)
    body_html = EMAIL_BODY_HTML.format(first_sentense, webapp, cost.id, invoice_link)
    recipents = get_recipents(email, cost)
    recipents = list(set(recipents + settings.INVOICE_APPROVAL_RECIPENTS.split(',')))
    send_email(recipents, subject, body_text, body_html)

EMAIL_SUBJECT = "Invoice({}): {}"

EMAIL_BODY_TEXT = ("{}\r\n"
             "To see the invoice, please sign in {}, and then go to "
             "Invoices page and find the invoice by id({}). "
             "Or if you have already signed in with 'Remember me' option checked, "
             "you can open the following link directly.\r\n{}"
            )

EMAIL_BODY_HTML = """<html>
<body>
  <p>{}</p>
  <p>To see the invoice, please sign in {}, and then go to Invoices page and find the invoice by id({}).</p>
  <p>
    Or if you have already signed in with <em>Remember me</em> option checked, you can open the 
    <a href='{}' target="_blank">invoice link</a> directly.
  </p>
</body>
</html>
"""
