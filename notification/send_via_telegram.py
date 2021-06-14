import configparser
import logging
from enum import (Enum, auto)

from telethon import (
    TelegramClient,
    errors,
    events,
    Button
)
from commons.models import UserOnTelegram, MessageSentOnTelegram

# enable logging
logging.basicConfig(
    # filename=f"log {__name__} KekrosVerifierBot.log",
    format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# get logger
logger = logging.getLogger(__name__)


config = configparser.ConfigParser()
config.read('api/.bot_env.ini')

bot_api_id = config['Telegram']['bot_api_id']
bot_api_hash = config['Telegram']['bot_api_hash']
bot_token = config['Telegram']['bot_token']

try:
    bot = TelegramClient(
        'verifier',
        bot_api_id,
        bot_api_hash
    ).start(bot_token=bot_token)
except Exception as e:
    logger.exception(str(e), exc_info=True)
else:
    bot.parse_mode = "md"
    operation_state = dict()

"""
todo:
    [ ] - run numbers_retriever and get all the numbers
    [ ] - get_id_from_tel_number() by running it every 10 secs
    [ ] - save all the numbers with their telegram_id into db
    [ ] - when msg to be sent comes, find the number in db, retrive the id and send the msg
    [x] - implement __get_item__() on the States class to solve the unsubscriptable error
fix:
    [ ] - it is getting stuck on the telegram part, it has to move on from that
hack:
    [ ] - perhaps a completely different setup with a completely new address
"""


class States(Enum):
    """
    States holds as an enum the states that the bot can be in. There are only two states allowed.
    The START state where a user just began interacting with the bot and PROVIDE_CONTACT where a user
    must provide his contact details.

    Args:
        super class Enum [Enum]: Generic enumeration.

    Returns:[ ] -
        [States]: The state that the bot will be in.
    """
    START = auto()
    PROVIDE_CONTACT = auto()

    def __getitem__(self):
        return str(self)


commands_dict = {'start_cmd': "/start", 'help_cmd': "/help"}


def save_num_and_id(user_phone_number, user_telegram_id):
    """
    save_num_and_id will be provided by the phone number and telegram id of a user
    and that will insert it into the db.

    Args:
        user_phone_number ([type]): [description]
        user_telegram_id ([type]): [description]
    """
    telegram_user_data = UserOnTelegram(tel_number=user_phone_number, telegram_id=int(user_telegram_id))
    telegram_user_data.save()


def get_id_from_tel_num():
    """
    get_id_from_tel_num will utilize telthon's get_input_entity() and get the telegram id
    of a user from the telephone number provided.
    """
    telegram_user_data = UserOnTelegram.objects.get()
    save_num_and_id()
    pass


def get_id_from_db(tel_num):
    user_tg_id = UserOnTelegram.objects.get(tel_num)
    return int(user_tg_id)


def send_message(user_tg_id, msg_text):
    user_entity = bot.get_input_entity(user_tg_id)
    bot.send_message(user_entity, msg_text, notify=True)


def send_to_user_telegram(sms_data):
    logger.info("sending via telegram", exec_info=True)
    tel_num = sms_data['number']
    user_tg_id = get_id_from_db(tel_num)
    if not user_tg_id:
        send_message(user_tg_id, sms_data['msg_text'])
    else:
        user_tg_id = get_id_from_tel_num(tel_num)
        send_message(user_tg_id, sms_data['msg_text'])


@bot.on(events.NewMessage)
async def register_tel_num_id_on_start(event):
    """
    register_tel_num_id_on_start will register users that /start the bot.

    Args:
        event [NewMessage]: an event triggered when a user sends any message that is new to the handler.
    """
    telegram_id = event.sender_id
    if event.raw_text.lower() == commands_dict['start_cmd']:
        logger.info(f"{telegram_id} has started the bot")
        operation_state[telegram_id] = {'state': States.START}
        await event.respond(
            "please share you contact with us so we can deliver the messages",
            buttons=Button.request_phone(text="share contact")
        )
        operation_state[telegram_id] = {'state': States.PROVIDE_CONTACT}
    elif event.raw_text.lower() == commands_dict['help_cmd']:
        help_msg = "This bot sends you the messages that were sent from Vamos Entertainment, " \
            "Habesha Sports Betting & Bet24 from this bot right here on telegram.\n\nGood Luck."
        await event.respond(help_msg, buttons=Button.clear())
    elif telegram_id in operation_state.keys():
        current_state = operation_state[telegram_id]['state']
        if current_state == States.PROVIDE_CONTACT and event.contact:
            contact_telegram_id = event.contact.user_id
            contact_tel_num = event.contact.phone_number
            save_num_and_id(contact_tel_num, contact_telegram_id)
            final_msg = "Thank you, you will now receive messages from Vamos Entertainment, " \
                "Habesha Sports Betting & Bet24 from this bot.\n\nGood Luck."
            await event.respond(final_msg, buttons=Button.clear())
            del operation_state[telegram_id]
        elif current_state == States.PROVIDE_CONTACT and not event.contact:
            await event.respond(
                "please share you contact with us so we can deliver the messages",
                buttons=Button.request_phone(text="share contact")
            )
            operation_state[telegram_id] = {'state': States.PROVIDE_CONTACT}
        elif not event.raw_text.lower() in commands_dict.values():
            unknown_msg = "Unknown command, try again.\n\nplease share you contact with us so we can deliver the messages"
            await event.respond(
                unknown_msg,
                buttons=Button.request_phone(text="share contact")
            )
            operation_state[telegram_id] = {'state': States.PROVIDE_CONTACT}
        else:
            await event.respond(
                "please share you contact with us so we can deliver the messages",
                buttons=Button.request_phone(text="share contact")
            )
            operation_state[telegram_id] = {'state': States.PROVIDE_CONTACT}
    else:
        await event.respond("You have to /start the bot", buttons=Button.clear())

with bot:
    bot.run_until_disconnected()


# class UserOnTelegram(models.Model):
#     tel_number = models.CharField(max_length=15, unique=True)
#     telegram_id = models.IntegerField(unique=True)
#     registered_date = models.DateTimeField(auto_now=True)
#     # delivery_status = models.BooleanField(default=False)

#     class Meta:
#         verbose_name_plural = "UsersOnTelegram"

#     def __str__(self):
#         return f"tel_num {self.tel_number} -- telegram_id {self.telegram_id}"


# class MessageSentOnTelegram(models.Model):
#     message_content = models.CharField(max_length=160)
#     sent_date = models.DateTimeField(auto_now=True)
#     sent_to = models.ForeignKey(UserOnTelegram, related_name="telegram_user", on_delete=models.PROTECT, related_query_name="telegram_msg_sent_user")

#     class Meta:
#         verbose_name_plural = "MessagesSentOnTelegram"

#     def __str__(self):
#         return f"message sent {self.message_content} -- sent to {self.sent_to}"
