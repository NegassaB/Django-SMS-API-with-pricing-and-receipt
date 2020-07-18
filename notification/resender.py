'''
This is intended as a quick and dirty fix...you must upgrade the system itself.
'''

from commons.models import SMSMessages
from datetime import datetime, timedelta
from notification.sender import sender

import argparse
import sys
from threading import Thread
import time

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--day_diff",
    type=int,
    default=1,
    help="What the max number of days it needs to go back to"
  )
  date_args = parser.parse_args()
  sys.stdout.write("received day difference")
  resender(date_args)



def resender(date_args):

  '''
  this function will get all the unsent smses from the db.
  the parameter is a day/s that it will need to go back
  to and search.
  '''

  timedif = datetime.now() - timedelta(days=args.day_diff)
  timedif = timedif.date()
  queryset = SMSMessages.objects.filter(delivery_status="False", sent_date__gte=timedif)
  for s in queryset:
    datat = {"number": s.sms_number_to, "msg_text": s.sms_content}
    sys.stdout.write("attempting to send...")
    try:
      flag, resp = sender(datat)
      if flag:
        sys.stdout.write("WWWWOOOOOOHOOOOO")
        s.delivery_status = "True"
        s.save()
        sys.stdout.write("db updated")
      else:
        sys.stdout.write("FUUUUUCKK")
    except Exception as e:
      sys.stdout.write("{}{}".format("exception,", e))
    finally:
      sys.stdout.write("finished")
  time.sleep(5)

t1 = Thread(target=resender, args=(date_args), daemon=True)
t1.start()


if __name__ == "__main__":
    main()
