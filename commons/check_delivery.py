from commons.models import SMSMessages


def check_delivery():
    keep_looping = True
    while keep_looping:
        gross = SMSMessages.objects.filter(
            sms_content="በሳምንቱ አጓጊ ጨዋታ PSG VS Bayern Munich ላይ ይወራረዱ፣ያሸንፉ\nቫሞስ ቤትስ\nwww.vamos.bet"
        )
        for g in gross:
            if g.sms_number_to == "+251911471207":
                print("sent to Bill")
                break
            elif g.sms_number_to == "+251913272636":
                print("sent to Selam")
                break
            elif g.sms_number_to == "+251910804769":
                print("sent to Wonde")
                break
            elif g.sms_number_to == "+251911985365":
                print("sent to GADD")
            else:
                pass
