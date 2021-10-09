'''
This is intended as a quick and dirty fix...you must upgrade the system itself.
'''

from commons.models import SMSMessages
from datetime import datetime, timedelta
from notification.sender import sender, telegram_sender

import sys
import time


def resender():

  '''
  this function will get all the unsent smses from the db.
  the parameter is a day/s that it will need to go back
  to and search.
  '''

  #timedif = datetime.now() - timedelta(days=date_args)
  #timedif = timedif.date()
  #queryset = SMSMessages.objects.filter(delivery_status=False, sent_date__gte=timedif)
  queryset = SMSMessages.objects.filter(
    sms_content__contains="activation code",
    sent_date__gte=datetime.now() - timedelta(seconds=5)
  )
  for s in queryset:
    datat = {"number": s.sms_number_to, "msg_text": s.sms_content}
    sys.stdout.write("attempting to send...\n")
    try:
      flag, resp = sender(datat)
      telegram_sender(datat)
      if flag:
        print("WWWWOOOOOOHOOOOO\n")
        s.delivery_status = "True"
        s.save()
        print("db updated\n")
      else:
        print("FUUUUUCKK\n")
    except Exception as e:
      print(f"exception, {e}")
    finally:
      print("finished\n")


if __name__ == "__main__":
  while 1:
    time.sleep(5)
    resender()
