import json
import logging
from typing import Union
from requests import request

from pydantic import ValidationError

from .message_schema import Updates

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)


def send_message(token: str,
                 chat_id: int,
                 text: str,
                 parse_mode: str = None,
                 buttons: list or None = None,
                 inline_keyboard: list or None = None,
                 one_time_keyboard: bool = True,
                 resize_keyboard: bool = True,
                 remove_keyboard: bool = False):
    payload = {
        "chat_id": chat_id,
        "text": text[:4095],
        "reply_markup": {
            "remove_keyboard": remove_keyboard
        }
    }
    if parse_mode:
        payload.update({"parse_mode": parse_mode})

    if buttons:
        # TODO hardcode
        keyboards = [[{"text": text}] for text in buttons]
        payload["reply_markup"].update({
            "keyboard": keyboards,
            "resize_keyboard": resize_keyboard,
            "one_time_keyboard": one_time_keyboard
        })

    if inline_keyboard:
        payload["reply_markup"].update({"inline_keyboard": inline_keyboard})

    headers = {
        "Content-Type": "application/json"
    }

    data = request("GET",
                   f"https://api.telegram.org/bot{token}/sendMessage",
                   headers=headers,
                   data=json.dumps(payload))

    # маскирование текста
    payload["text"] = "*******"

    log.debug("request with payload: %s success delivered to tlg", payload)

    return data


def get_updates(token: str, offset: int) -> Union[Updates, int]:
    headers = {
        "Content-Type": "application/json"
    }
    data = request("GET",
                   f"https://api.telegram.org/bot{token}/getUpdates?offset={offset}",
                   headers=headers)

    log.info(f"bot with token - {token} gets update with status - {data.status_code}")

    if data.status_code == 200:
        try:
            response = Updates(**data.json())
            return response
        except ValidationError as e:
            return -1
    else:
        return -1
