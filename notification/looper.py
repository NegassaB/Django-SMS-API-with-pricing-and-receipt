from commons.models import SMSMessages
from notification.resender import resender
from datetime import datetime
import time

def looper(time_diff):
    '''
    pass in a datetime object containing the current date that you want to send.
    '''
    queryset = SMSMessages.objects.filter(delivery_status=False, sent_date__date=time_diff)
    if queryset.count() != 0:
        print("sending from loop\n")
<<<<<<< HEAD
        time.sleep(5)
=======
        time.sleep(2)
>>>>>>> 400e7f12bda415bb9ea31e0959b4c786c29abc20
        resender(1)
    else:
        time.sleep(1)
        print("looping\n")
        return


def kicker():
    while True:
        x = datetime.now().date()
<<<<<<< HEAD
        time.sleep(2)
=======
>>>>>>> 400e7f12bda415bb9ea31e0959b4c786c29abc20
        looper(x)
        if datetime.now().date() != x:
            print("\n\trestarting script")
            continue

