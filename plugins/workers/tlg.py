import logging

from queue import Queue
from time import sleep

# try:
from ..tlg import send_message
from ..message_schema import Request
from ..cache.storage import memory
# except Exception as e:
#     from plugins.tlg import send_message
#     from message_schema import Request
#     from plugins.cache.storage import memory

transport = Queue()

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)


def start_tlg_worker():
    while True:
        try:
            request: Request = transport.get_nowait()
            list_of_users = memory.get_valid_users(request.DATA.bot_type)
            token = memory.get_token_by_bot_name(request.DATA.bot_type)
            if len(list_of_users) > 0 and len(token) > 0:
                for chat_id in memory.get_valid_users(request.DATA.bot_type):
                    data = send_message(
                            token=token,
                            text=request.DATA.log_info,
                            chat_id=chat_id
                    )
                    if not data.ok:
                        log.info(
                            f"something wrong, problems with bot name - {request.DATA.bot_type} or token - "
                            f"{token}")

            else:
                log.info(f"something wrong, we don't have users with bot name - {request.DATA.bot_type} or token - "
                         f"{token}")
        except Exception as e:
            pass
        sleep(0.5)
    # запрашиваем данные по пользователям
