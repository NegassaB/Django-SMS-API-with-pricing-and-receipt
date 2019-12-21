from django.shortcuts import render
from commons.models import SMSUser, SMSMessages, Invoice
from commons.serializers import InvoiceSerialzer

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

def generate_invoice(request, username, template_name):
    user_to_invoice = SMSUser.objects.get(username=username)
    user_invoice = Invoice(invoice_to=user_to_invoice)
    # TODO you have to figure out how to get the company name of each users on the SMSMessages table
    # all_sms_sent = SMSMessages.objects.all().filter()

    company_to_invoice = user_to_invoice.company_name
    company_tin = user_to_invoice.company_tin
    account = user_to_invoice.pk
    user_email = user_to_invoice.email
    all_users_in_company = SMSUser.objects.filter(company_name=company_to_invoice)
    user_invoice.save()
    invoice_number = user_invoice.pk
    paid_status = user_invoice.payment_status
    #TODO use something else other than a dictionary that can hold the username, the company and the total sent by that user in the month
    all_sms_sent_by_users = {}
    for user in all_users_in_company:
        #TODO you can get the month automatically by calling datetime.now.month()
        # TODO you can run the code at the begining of each month by doing:
        # TODO x = date.today() then x = x.replace(day=1) 
        total_sent_by_single_user = SMSMessages.objects.filter(
            sending_user=user,
            delivery_status="True",
            sent_date__year=datetime.now().year,
            sent_date__month = datetime.now().month - 2
            )
        all_sms_sent_by_users = {
            "all_sms_sent": [
                {
                "user": user,
                "total_sent_single_user": total_sent_by_single_user.count(),
                "company_name": company_to_invoice
                }
            ]
        }
    total_amount_sent = SMSMessages.objects.filter(
        sent_date__year = datetime.now().year,
        sent_date__month = 10,
        # sent_date__month = datetime.now().month - 1,
        sending_user__company_name=company_to_invoice
    )
    
    ret_val = render(
        request,
        template_name=template_name,
        context={
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
            "payment_status": paid_status,
        }
        )
    
    return ret_val

        # TODO return a pdf render of the template_name with all the necessary data inserted
