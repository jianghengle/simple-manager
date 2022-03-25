import os, io
import PyPDF2
from django.conf import settings
from ..models.attachment import Attachment
from .s3_service import download_file, upload_file, copy_object, get_object_content
from .sharepoint_service import save_to_sharepoint
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

def approve_cost(cost):
    download_file('/tmp/waterprint.pdf', settings.S3_BUCKET, 'waterprint.pdf')
    waterprint_file = open('/tmp/waterprint.pdf', 'rb')
    waterprint_pdf = PyPDF2.PdfFileReader(waterprint_file)
    waterprint_page = waterprint_pdf.getPage(0)
    new_attachment_ids = []

    (output_pdf, other_attachments, input_file_paths, input_files) = collect_pdf_and_others(cost, waterprint_page)

    new_attachment_ids.append(save_main_pdf(cost, output_pdf, other_attachments))
    for i in range(len(other_attachments)):
        new_attachment_ids.append(save_other_attachment(i, other_attachments[i], cost))
    cost.attachments = ','.join(new_attachment_ids)
    cost.save()

    waterprint_file.close()
    os.remove('/tmp/waterprint.pdf')

    for input_file in input_files:
        input_file.close()
    for input_file_path in input_file_paths:
        os.remove(input_file_path)

def save_main_pdf(cost, output_pdf, other_attachments):
    vendor_name = replace_special_chars(cost.vendor_name)
    invoice_number = replace_special_chars(cost.invoice_number)
    subsidiary = replace_special_chars(cost.subsidiary)
    pdf_name = '_'.join([vendor_name, invoice_number, subsidiary, 'id(' + str(cost.id) + ')'])
    if len(other_attachments):
        pdf_name = pdf_name + '(1).pdf'
    else:
        pdf_name = pdf_name + '.pdf'

    temp_output_file_path = '/tmp/output-' + pdf_name
    output_file = open(temp_output_file_path, 'wb')
    output_pdf.write(output_file)
    output_file.close()

    stage = os.environ.get('STAGE', 'development')
    new_key = os.path.join(stage, 'attachments', 'approved', str(cost.id), pdf_name)
    upload_file(temp_output_file_path, settings.S3_BUCKET, new_key)

    new_attachment = Attachment()
    new_attachment.name = pdf_name
    new_attachment.s3_bucket = settings.S3_BUCKET
    new_attachment.s3_key = new_key
    new_attachment.created_by = 'System'
    new_attachment.save()

    with open(temp_output_file_path, 'rb') as content_file:
        file_content = content_file.read()
        save_to_sharepoint(file_content, pdf_name, vendor_name)

    os.remove(temp_output_file_path)

    return str(new_attachment.id)


def save_other_attachment(i, attachment, cost):
    _, ext = os.path.splitext(attachment.name)
    vendor_name = replace_special_chars(cost.vendor_name)
    invoice_number = replace_special_chars(cost.invoice_number)
    subsidiary = replace_special_chars(cost.subsidiary)
    filename = '_'.join([vendor_name, invoice_number, subsidiary, 'id(' + str(cost.id) + ')']) + '(' + str(i + 2) + ')' + ext
    source_bucket = attachment.s3_bucket
    source_key = attachment.s3_key
    (path, name) = os.path.split(source_key)
    stage = os.environ.get('STAGE', 'development')
    target_key = os.path.join(stage, 'attachments', 'approved', str(cost.id), filename)
    copy_object(source_bucket, source_key, source_bucket, target_key)

    new_attachment = Attachment()
    new_attachment.from_json(attachment.to_json())
    new_attachment.s3_key = target_key
    new_attachment.name = filename
    new_attachment.save()

    file_content = get_object_content(source_bucket, target_key)
    save_to_sharepoint(file_content, filename, vendor_name)
    return str(new_attachment.id)



def collect_pdf_and_others(cost, waterprint_page):
    output_pdf = PyPDF2.PdfFileWriter()
    other_attachments = []
    input_file_paths = []
    input_files = []
    for s in cost.attachments.split(','):
        if not s:
            continue
        attachment = Attachment.objects.get(pk=s.strip())
        _, ext = os.path.splitext(attachment.name)
        if ext.lower() == '.pdf':
            try:
                (path, name) = os.path.split(attachment.s3_key)
                temp_input_file_path = '/tmp/input-' + name
                input_file_paths.append(temp_input_file_path)
                download_file(temp_input_file_path, attachment.s3_bucket, attachment.s3_key)
                input_file = open(temp_input_file_path, 'rb')
                input_files.append(input_file)
                input_pdf = PyPDF2.PdfFileReader(input_file)
                for i in range(input_pdf.getNumPages()):
                    pdf_page = input_pdf.getPage(i)
                    pdf_page.mergePage(waterprint_page)
                    output_pdf.addPage(pdf_page)
            except Exception as e:
                print(e)
                other_attachments.append(attachment)
        else:
            other_attachments.append(attachment)
    write_description_to_pdf(cost, waterprint_page, output_pdf)
    return (output_pdf, other_attachments, input_file_paths, input_files)


def write_description_to_pdf(cost, waterprint_page, output_pdf):
    if not cost.description:
        return

    temp_file_path = '/tmp/description-' + str(cost.id) + '.pdf'
    doc = SimpleDocTemplate(temp_file_path, pagesize=LETTER, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    doc.build([Paragraph(cost.description.replace("\n", "<br />"), getSampleStyleSheet()['Normal']),])

    input_file = open(temp_file_path, 'rb')
    input_pdf = PyPDF2.PdfFileReader(input_file)
    for i in range(input_pdf.getNumPages()):
        pdf_page = input_pdf.getPage(i)
        pdf_page.mergePage(waterprint_page)
        output_pdf.addPage(pdf_page)
    input_file.close()
    os.remove(temp_file_path)

def replace_special_chars(s):
    special_chars = ['~', '"', '#', '%', '&', '*', ':', '<', '>', '?', '/', '\\', '{', '|', '}', '.']
    output = s
    for c in special_chars:
        output = output.replace(c, '-')
    return output

