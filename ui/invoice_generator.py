from django.shortcuts import render
from commons.models import SMSUser, SMSMessages, Invoice
from commons.serializers import InvoiceSerialzer

from django.template.loader import get_template
from django.conf import settings
from django.http import HttpResponse

from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration
import tempfile

from datetime import datetime, date

"""
don't know how to do it yet, but it should:
1. get the company from the SMSMessages table
2. get all username's that have sent those smses
3. get all the messages that are sent with in that month
4. calculate the total price by all_sms_sent * price_of_one_sms
5. display in what time it should be paid (one week)
6. save to user account under invoices section as file and pdf
"""

#TODO run this in a separate thread
def generate_invoice(request, username, template_name):
    user_to_invoice = SMSUser.objects.get(username=username)
    user_invoice = Invoice(invoice_to=user_to_invoice)

    company_to_invoice = user_to_invoice.company_name
    company_tin = user_to_invoice.company_tin
    account = user_to_invoice.pk
    user_email = user_to_invoice.email
    all_users_in_company = SMSUser.objects.filter(company_name=company_to_invoice)
    user_invoice.save()
    invoice_number = user_invoice.pk
    paid_status = user_invoice.payment_status

    # All the sms sent by each users is retrieved from the database and put into
    # the all_sms_sent_by_user dictionary object with a name of "all_sms_sent"
    # that contains a list of dictionary objects that contain the user that sent the smses,
    # the total_sent_smses. The company_name of the user can be derived from the user
    # attribute.

    all_sms_sent_by_users = {}

    for user in all_users_in_company:
        # TODO you can run the code at the begining of each month by doing:
        # TODO x = date.today() then x = x.replace(day=1) 
        total_sent_by_single_user = SMSMessages.objects.filter(
            sending_user=user,
            delivery_status="True",
            sent_date__year=datetime.now().year,
            # sent_date__month = 10
            sent_date__month = datetime.now().month - 1
            )
        all_sms_sent_by_users = {
            "all_sms_sent": [
                {
                "user": user,
                "total_sent_single_user": total_sent_by_single_user.count()
                }
            ]
        }
    total_amount_sent = SMSMessages.objects.filter(
        sent_date__year = datetime.now().year,
        sent_date__month = 10,
        # sent_date__month = datetime.now().month - 1,
        sending_user__company_name=company_to_invoice
    )

    context_object =  {
        "username": user_to_invoice,
        "company_name": company_to_invoice,
        "account": account,
        "invoice_number": invoice_number,
        "tin": company_tin,
        "email": user_email,
        "bill_month": datetime.now().month - 1,
        "all_sms_sent": all_sms_sent_by_users,
        "total_amount_sent": total_amount_sent.count(),
        "vat": total_amount_sent.count() * 0.70 * 0.15,
        "total_price": total_amount_sent.count() * 0.70 * 1.15, 
        "payment_status": paid_status
    }
    # html_to_render = render(request=request, template_name='ui/invoice.html', context=context_object)
    rendered_html = get_template(template_name).render(
       context_object,
        request
    ).encode(encoding='UTF-8')
    
    font_config = FontConfiguration()
    pdf_file = HTML(string=rendered_html, base_url=request.build_absolute_uri())
    pdf_file.render()
    pdf_container = pdf_file.write_pdf(
        stylesheets=[
            CSS(string='@page {size: A4; margin: 0.1cm;}'
                'ui' + settings.STATIC_URL + 'ui/css/bootstrap.min.css',
                _check_mime_type=True,
                font_config=font_config,
                encoding='UTF-8',
                media_type='screen'
            )
        ],
        presentational_hints=True,
        font_config=font_config,
    )
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'filename=Invoice ' + company_to_invoice + str(datetime.now().month) + '.pdf'
    response['Content-Transfer-Encoding'] = 'UTF-8'
    with tempfile.NamedTemporaryFile(delete=True) as pdf_writer:
        pdf_writer.write(pdf_container)
        pdf_writer.flush()
        pdf_writer = open(pdf_writer.name, 'rb')
        response.write(pdf_writer.read())
    return response
    # return html_to_render
    
    # return ret_val
