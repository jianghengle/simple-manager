import os, io
import PyPDF2
from django.conf import settings
from ..models.attachment import Attachment
from .s3_service import download_file, upload_file, copy_object

def add_waterprints(cost):
    waterprint_file = None
    for s in cost.attachments.split(','):
        attachment = Attachment.objects.get(pk=s.strip())
        _, ext = os.path.splitext(attachment.name)
        if ext.lower() == '.pdf':
            if waterprint_file == None:
                download_file('/tmp/waterprint.pdf', settings.S3_BUCKET, 'waterprint.pdf')
                waterprint_file = open('/tmp/waterprint.pdf', 'rb')
                waterprint_pdf = PyPDF2.PdfFileReader(waterprint_file)
                waterprint_page = waterprint_pdf.getPage(0)
            try:
                add_waterprint(cost, attachment, waterprint_page)
            except:
                copy_attachment_to_approved(cost, attachment)
        else:
            copy_attachment_to_approved(cost, attachment)
    if waterprint_file != None:
        waterprint_file.close()
        os.remove('/tmp/waterprint.pdf')
    

def add_waterprint(cost, attachment, waterprint_page):
    (path, name) = os.path.split(attachment.s3_key)

    temp_input_file_path = '/tmp/input-' + name
    download_file(temp_input_file_path, attachment.s3_bucket, attachment.s3_key)
    input_file = open(temp_input_file_path, 'rb')
    input_pdf = PyPDF2.PdfFileReader(input_file)
    output_pdf = PyPDF2.PdfFileWriter()
    for i in range(input_pdf.getNumPages()):
        pdf_page = input_pdf.getPage(i)
        pdf_page.mergePage(waterprint_page)
        output_pdf.addPage(pdf_page)
    
    temp_output_file_path = '/tmp/output-' + name
    output_file = open(temp_output_file_path, 'wb')
    output_pdf.write(output_file)

    input_file.close()
    output_file.close()

    new_key = os.path.join(path, 'approved', str(cost.id), name)
    upload_file(temp_output_file_path, attachment.s3_bucket, new_key)

    os.remove(temp_input_file_path)
    os.remove(temp_output_file_path)

    attachment.s3_key = new_key
    attachment.save()

def copy_attachment_to_approved(cost, attachment):
    source_bucket = attachment.s3_bucket
    source_key = attachment.s3_key
    (path, name) = os.path.split(source_key)
    target_key = os.path.join(path, 'approved', str(cost.id), name)
    copy_object(source_bucket, source_key, source_bucket, target_key)