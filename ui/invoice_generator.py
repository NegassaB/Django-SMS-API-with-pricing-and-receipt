from django.shortcuts import render
from commons.models import SMSUser, SMSMessages, Invoice
from commons.serializers import InvoiceSerialzer

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
    # invoice_serializer = InvoiceSerialzer(data={"invoice_to": username})
    # if invoice_serializer.is_valid():
    #     invoice_number = invoice_serializer.validated_data["invoice_number"]
    #     invoice_object = invoice_serializer.save()
    #     user_to_invoice = invoice_serializer.validated_data["invoice_to"]
    #     company_to_invoice = user_to_invoice.company_name
    #     company_tin = user_to_invoice.company_tin
    #     user_account = user_to_invoice.pk
    #     paid_status = invoice_serializer.validated_data["payment_status"]
    #     all_users_in_company = SMSUser.objects.filter(company_name=company_to_invoice)

    #     ret_val = render(
    #         request,
    #         template_name=template_name,
    #         context={
    #             "username": user_to_invoice,
    #             "company_name": company_to_invoice,
    #             "account": account,
    #             "Invoice_number": invoice_number,
    #             "tin": company_tin,
    #             "email": user_email,
    #             "bill_month": "not yet defined",
    #             "due_date": "not yet defined",
    #             "users_that_sent_sms": {[un for un in all_users_in_company.username]},
    #             "VAT": "not yet defined",
    #             "Total": "not yet defined",
    #             "payment_status": paid_status,
    #         }
    #     )
    

    user_to_invoice = SMSUser.objects.get(username=username)
    user_invoice = Invoice(invoice_to=user_to_invoice)
    # user_invoice = Invoice(data)
    # TODO you have to figure out how to get the company name of each users on the SMSMessages table
    # all_sms_sent = SMSMessages.objects.all().filter()

    company_to_invoice = user_to_invoice.company_name
    company_tin = user_to_invoice.company_tin
    account = user_to_invoice.pk
    user_email = user_to_invoice.email
    all_users_in_company = SMSUser.objects.all().filter(company_name="company_to_invoice")
    user_invoice.save()
    invoice_number = user_invoice.pk
    paid_status = user_invoice.payment_status


    ret_val = render(
        request,
        template_name=template_name,
        context={
            "username": user_to_invoice,
            "company_name": company_to_invoice,
            "account": account,
            "Invoice_number": invoice_number,
            "tin": company_tin,
            "email": user_email,
            "bill_month": "not yet defined",
            "due_date": "not yet defined",
            "users_that_sent_sms": [un for un in all_users_in_company],
            "VAT": "not yet defined",
            "Total": "not yet defined",
            "payment_status": paid_status,
        }
        )

        # TODO return a pdf render of the template_name with all the necessary data inserted
