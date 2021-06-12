import csv
from commons.models import SMSMessages

def retriever():
    q = SMSMessages.objects.values('sms_number_to').distinct()
    with open('total_numbers.csv', 'w') as data:
        csv_writer = csv.writer(data)
        for d in q:
            for k, v in d.items():
                csv_writer.writerow([v])

