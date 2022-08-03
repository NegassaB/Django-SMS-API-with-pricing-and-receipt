from commons.models import SMSUser, SMSMessages
import datetime


def generator():
    current_datetime = datetime.datetime.now()
    year = current_datetime.year
    month = current_datetime.month - 1
    all_users = SMSUser.objects.all()
    for user in all_users:
        sent_sms = SMSMessages.objects.filter(sending_user=user, sent_date__year=year, sent_date__month=month)
        print(f"sending_user -- {user.username} sent_sms {sent_sms.count()}")


if __name__ == "__main__":
    generator()
