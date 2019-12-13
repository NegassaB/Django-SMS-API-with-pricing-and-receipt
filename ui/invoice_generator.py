from django.shortcuts import render
from commons.models import Invoice, SMSUser, SMSMessages

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
    invoice = Invoice(username)
    user_to_invoice = SMSUser.objects.get(username)
    # TODO you have to figure out how to get the company name of each users on the SMSMessages table
    # all_sms_sent = SMSMessages.objects.all().filter()

    company_to_invoice = user_to_invoice.company_name
    company_tin = user_to_invoice.company_tin
    invoice_number = invoice.invoice_number
    account = company_to_invoice.pk
    user_email = user_to_invoice.emali
    paid_status = invoice.payment_status
    all_users_in_company = SMSUser.objects.all().filter(company_name="company_to_invoice")


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
            "users_that_sent_sms": "not yet defined",
            "VAT": "not yet defined",
            "Total": "not yet defined",
            "payment_status": paid_status,
        }
        )

        # TODO return a pdf render of the template_name with all the necessary data inserted
