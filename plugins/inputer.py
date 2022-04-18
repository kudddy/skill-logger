import logging
from threading import Thread

from pydantic import ValidationError

from .workers.tlg import start_tlg_worker, transport
from .workers.updater import get_updates_from_tlg
from .message_schema import Request
from .cache.storage import memory

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)

# starts thread with telegram workers, who send logs to the consumers
tgl_thread = Thread(target=start_tlg_worker)
tgl_thread.start()

# get all valid tokens from database
# TODO проверка на кол-во одновременно запущенных потоков

[Thread(target=get_updates_from_tlg, args=(x,)).start() for x in memory.get_all_tokens()]

example_request = {
    "MESSAGE_NAME": "LOGGER_INFO",
    "DATA": {
        "log_info": "RP123| 14.08.2022 15:00| 200",
        "bot_type": "sberauto"
    }
}


def inputter(request: dict):
    log.debug(f'start process message with payload - {request}')

    try:
        request = Request(**request)
    except ValidationError as e:
        log.info(str(e))
        return {
            "MESSAGE_NAME": "LOGGER_INFO",
            "CODE": 403,
            "STATUS": False,
            "DATA": {
                "desc": "validation error"
            }
        }
    # this method put job in queen for send message to consumers
    if request.MESSAGE_NAME == "LOGGER_INFO":

        if memory.check_bot_exist(request.DATA.bot_type):

            transport.put(request)

            return {
                "MESSAGE_NAME": "LOGGER_INFO",
                "CODE": 200,
                "STATUS": True,
                "DATA": {
                    "desc": "ok, job start"
                }
            }
        else:
            return {
                "MESSAGE_NAME": "LOGGER_INFO",
                "CODE": 404,
                "STATUS": False,
                "DATA": {
                    "desc": f"something, bot - {request.DATA.bot_type} is not exist."
                }
            }
    # this method puts the consumers in the list that the log will send to
    elif request.MESSAGE_NAME == "PUT_CONSUMERS_ID":

        return {
            "MESSAGE_NAME": "PUT_CONSUMERS_ID",
            "CODE": 200,
            "STATUS": True,
            "DATA": {
                "desc": "ok, consumers added"
            }
        }

# thread check notication from tlg

# администратор выдает токен пользователю

# пользователь отправляет токен, токен ассоциируется с навык, навык ассоциируется с токеном бота

# add user_id, chat, id, token to table


# требуется создать кэш который хранит данные и каждый пять минут обновляет их из базы
