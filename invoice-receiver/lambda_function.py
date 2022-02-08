import os, random, string
import json
import urllib.parse
import urllib.request
import boto3
import email

FIELDS = ['subject', 'description', 'reviewer', 'amount', 'tags', 'comment']
BUCKET = 'simple-manager-web-app'
KEY_PREFIX = 'production/attachments/'
SERVER = 'https://myapi.vanityart.com'

s3 = boto3.client('s3')

def get_email_subject(message):
    return message['subject'].strip()

def get_email_from(message):
    email_from = message['from'].strip().lower()
    ss = email_from.split('<')
    if len(ss) == 1:
        return ss[0]
    return ss[len(ss) - 1].split('>')[0]

def get_email_text(message):
    text = ''
    if message.is_multipart():
        for part in message.walk():
            if part.get_content_type() == 'text/plain':
                text = text + part.get_payload(decode=True).decode('utf-8')
    else:
        text = message.get_payload(decode=True).decode('utf-8')
    return text

def get_invoice_overrides(text):
    overrides = {}
    (content, _) = text.split('-----', 1)
    multiple_line_field = ''
    for line in content.split('\n'):
        head = line
        tail = ''
        if ':' in line:
            (head, tail) = line.split(':', 1)
        field = head.strip().lower()
        value = tail.strip()
        if field in FIELDS:
            if field == 'reviewer':
                overrides['reviewers'] = value
            elif field == 'amount':
                overrides['amount'] = float(value)
            else:
                overrides[field] = value
            if field == 'description' or field == 'comment':
                multiple_line_field = field
            else:
                multiple_line_field = ''
        elif multiple_line_field:
            if overrides[multiple_line_field]:
                overrides[multiple_line_field] = overrides[multiple_line_field] + '\n' + line
            else:
                overrides[multiple_line_field] = line
    return overrides

def get_attachments(message):
    attachments = {}
    if message.is_multipart():
        for part in message.walk():
            filename = part.get_filename()
            if filename:
                _, ext = os.path.splitext(filename)
                if ext.lower() == '.pdf':
                    attachments[filename] = part.get_payload(decode=True)
    return attachments
    
def get_random_string(n):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))
    
def save_attachment(email_from, token, filename, filebody):
    name, ext = os.path.splitext(filename)
    key = KEY_PREFIX + name + '.' + get_random_string(16) + ext
    s3.put_object(Body=filebody, Bucket=BUCKET, Key=key)
    data = {
        'name': filename,
        's3Bucket': BUCKET,
        's3Key': key,
        'createdBy': email_from
    }
    attachment = url_post('/myapp/create-attachment/', data, token=token)
    return attachment['id']
    
def url_get(path, token=None):
    req =  urllib.request.Request(SERVER + path)
    if token:
        req.add_header('Authorization', 'Token ' + token)
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read().decode("utf-8"))

def url_post(path, data, token=None):
    req_data = urllib.parse.urlencode(data).encode()
    req =  urllib.request.Request(SERVER + path, data=req_data)
    if token:
        req.add_header('Authorization', 'Token ' + token)
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read().decode("utf-8"))

def get_auth_token():
    data = {'username': 'invoice@vanityart.com', 'password': os.environ['INVOICE_USER_PASSWORD']}
    user = url_post('/myapp/api-token-auth/', data)
    return user['token']

# lambda handler: program entry
def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'], encoding='utf-8')
        response = s3.get_object(Bucket=bucket, Key=key)
        message = email.message_from_bytes(response['Body'].read())
        handle_email_message(message)
    print('done')

def handle_email_message(message):
    subject = get_email_subject(message)
    email_from = get_email_from(message)
    token = get_auth_token()
    all_emails = url_get('/myapp/get-all-emails/', token=token)
    if email_from not in all_emails:
        print('Invoice from an unknown user: ' + email_from)
        return
    
    description = get_email_text(message)
    overrides = get_invoice_overrides(description)

    attachments = get_attachments(message)
    attachment_ids = []
    for filename in attachments:
        attachment_id = save_attachment(email_from, token, filename, attachments[filename])
        attachment_ids.append(str(attachment_id))
    
    invoice_data = {
        'subject': subject,
        'description': description,
        'createdBy': email_from,
        'status': 'Open',
        'closedBy': '',
        'reviewers': email_from,
        'amount': 0,
        'tags': '',
        'comment': '',
        'attachments': ','.join(attachment_ids),
        'sendEmail': True
    }
    for k in overrides:
        invoice_data[k] = overrides[k]
    invoice = url_post('/myapp/create-cost/', invoice_data, token=token)
    print(invoice)
