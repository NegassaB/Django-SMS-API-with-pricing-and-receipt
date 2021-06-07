import csv
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
django.setup()

from commons.models import SMSMessages


def retriever():
    q = SMSMessages.objects.values('sms_number_to').distinct()
    with open('/home/gadd/total_numbers.csv', 'w') as data:
        csv_writer = csv.writer(data)
        for d in q:
            for k, v in d.items():
                csv_writer.writerow([v])


if __name__ == "__main__":
    retriever()
