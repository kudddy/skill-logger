import logging

from threading import Thread
from time import sleep

from ..tlg import get_updates, send_message
from ..db.query import insert_valid_user, insert_log_auth_data
from ..cache.storage import memory

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)

SUBSCRIBE = "subscription"

REG = "register"

UNKNOWN = "unknown"


class Behaviour:
    def __init__(self):
        pass

    def what_user_want(self, update, token: str):
        # TODO i catch errors in this line
        text_from_user = update.message.text.split("|")

        # валидация входящего сообщения
        if len(text_from_user) == 2 and text_from_user[1].strip() == SUBSCRIBE:
            self._subscribe_user(update, token)
        elif len(text_from_user) == 5 and text_from_user[4].strip() == REG:
            self._register_bot(update=update,
                               token=token)
        else:
            self._unknown_intent(update=update,
                                 token=token)

    @staticmethod
    def _subscribe_user(update, token: str):
        auth_uid = update.message.text.split("|")[0].strip()

        bot_name = memory.check_user(auth_uid=auth_uid, token=token)

        if bot_name == "not_valid_user":
            # отправляем wrong message
            send_message(token=token,
                         chat_id=update.message.chat.id,
                         text="oh no, you pass is weird❌")
        else:
            # TODO
            # in this place we should update cache

            if memory.user_already_subscribe(bot_name=bot_name,
                                             chat_id=str(update.message.chat.id)):
                # send what all is fine
                send_message(token=token,
                             chat_id=update.message.chat.id,
                             text="user already subscribe❌")
            else:
                memory.update_cache_with_valid_users(chat_id=update.message.chat.id,
                                                     bot_name=bot_name)

                # send valid chat id to database
                insert_valid_user(bot_name=bot_name,
                                  chat_id=update.message.chat.id)

                # send what all is fine
                send_message(token=token,
                             chat_id=update.message.chat.id,
                             text="ok, now you have access to logs✅")

    @staticmethod
    def _register_bot(update, token: str):

        # TODO we should valid uuid

        split_user_request = update.message.text.split("|")
        auth_uid: str = split_user_request[0].strip()
        bot_name: str = split_user_request[1].strip()
        tlg_token: str = split_user_request[2].strip()
        new_auth_uid: str = split_user_request[3].strip()

        # TODO control count of users
        if memory.check_permission_to_add_new_bot(auth_uid=auth_uid):

            # TODO we don't update cache
            # send data to base with new auth data
            insert_log_auth_data(tlg_token=tlg_token,
                                 auth_token=new_auth_uid,
                                 bot_name=bot_name)

            memory.update_memory_auth_cache(tlg_token=tlg_token,
                                            auth_token=new_auth_uid,
                                            bot_name=bot_name)

            # send message that all is fine
            send_message(token=token,
                         chat_id=update.message.chat.id,
                         text="ok, new bot succes added to notification✅")

            # start thread with new job
            Thread(target=get_updates_from_tlg, args=(tlg_token,)).start()
        else:
            # отправляем wrong message
            send_message(token=token,
                         chat_id=update.message.chat.id,
                         text="oh no, you pass is weird❌")

    @staticmethod
    def _unknown_intent(update, token: str):
        # отправляем wrong message
        send_message(token=token,
                     chat_id=update.message.chat.id,
                     text="oh no, i don't known what you want❌")


behaviour = Behaviour()


def get_updates_from_tlg(token: str):
    log.info(f"start thread which check updates from bot with token - {token}")
    # every 0.5 sec check updates from tlg
    offset = 0
    while True:
        resp = get_updates(token, offset)
        if resp != -1 and resp.ok and len(resp.result) > 0:
            #
            for updates in resp.result:
                try:
                    behaviour.what_user_want(update=updates,
                                             token=token)
                except Exception as e:
                    log.info(f"troubles, error - {str(e)}")

                offset = updates.update_id + 1

        sleep(0.5)
