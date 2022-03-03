import os
from django.conf import settings
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.files.file_system_object_type import FileSystemObjectType
from office365.runtime.client_request_exception import ClientRequestException
from office365.sharepoint.documentmanagement.document_set import DocumentSet

SHAREPOINT_SITE = 'https://vanityart.sharepoint.com/'

stage = os.environ.get('STAGE', 'development')
INVOICE_PATH_BASE = '/Shared Documents/TestInvoiceSystem' if stage == 'development' else '/Shared Documents/ACCOUNTING DEPT/Accounting/AP/Approved Invoices'

def get_sharepoint_client():
    client_id = settings.SHAREPOINT_CLIENT_ID
    client_secret = settings.SHAREPOINT_CLIENT_SECRET
    if client_id and client_secret:
        client_credentials = ClientCredential(client_id, client_secret)
        return ClientContext(SHAREPOINT_SITE).with_credentials(client_credentials)

def save_to_sharepoint(file_content, filename, savepath):
    client = get_sharepoint_client()
    if client:
        path = os.path.join(INVOICE_PATH_BASE, savepath)
        folder = get_sharepoint_folder(client, path)
        folder.upload_file(filename, file_content).execute_query()


def get_sharepoint_folder(client, path):
    folder = try_get_folder(client, path)
    if folder is None:
        create_folder(client, path)
        folder = try_get_folder(client, path)
    return folder

def try_get_folder(client, path):
    try:
        return client.web.get_folder_by_server_relative_url(path).get().execute_query()
    except ClientRequestException as e:
        if e.response.status_code == 404:
            return None
        else:
            raise ValueError(e.response.text)

def create_folder(client, path):
    client.web.folders.add(path)
