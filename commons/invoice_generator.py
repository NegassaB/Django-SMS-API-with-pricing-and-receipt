from commons.models import SMSUser, SMSMessages
import datetime


def generator(year=None, month=None):
    current_datetime = datetime.datetime.now()
    if not year:
        year = current_datetime.year
    if not month:
        month = current_datetime.month
    all_users = SMSUser.objects.all()
    for user in all_users:
        sent_sms = SMSMessages.objects.filter(sending_user=user, sent_date__year=year, sent_date__month=month)
        if sent_sms.count() == 0:
            continue
        if user.username == "ActivBetUser1" or user.username == "UTopUser" or user.username == "ChampionBet":
            sent_sms = sent_sms.filter(delivery_status=True)
        print(f"sending_user -- {user.username} sent_sms {sent_sms.count()}")


if __name__ == "__main__":
    generator()
