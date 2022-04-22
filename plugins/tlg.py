import json
import logging
import requests

from typing import Union
from requests import request
from time import sleep

from pydantic import ValidationError

from .message_schema import Updates

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

log.setLevel(logging.INFO)


class Retry:
    def __init__(self, retry=5, time_to_sleep=15):
        self._retry = retry
        self._count = 0
        self._time_to_sleep = time_to_sleep

    def send(self, method: str,
             url: str,
             headers: dict):

        try:
            data = request(method,
                           url,
                           headers=headers)
            return data

        except requests.exceptions.ConnectionError:
            log.info("problems with request, start retry")

            self._count += 1

            if self._retry > self._count:
                sleep(self._time_to_sleep)
                return self.send(method, url, headers)
            else:
                return -1


retry = Retry()


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

    if data.status_code != 200:
        try:
            log.info(f"send message request have problems and response is - {data.json()}")
        except Exception as e:
            log.info(f"can't decode json from response, error - {str(e)}")

    # маскирование текста
    payload["text"] = "*******"

    log.debug("request with payload: %s success delivered to tlg", payload)

    return data


def get_updates(token: str, offset: int) -> Union[Updates, int]:
    headers = {
        "Content-Type": "application/json"
    }
    # data = request("GET",
    #                f"https://api.telegram.org/bot{token}/getUpdates?offset={offset}",
    #                headers=headers)

    data = retry.send("GET",
                      f"https://api.telegram.org/bot{token}/getUpdates?offset={offset}",
                      headers=headers)

    if data == -1:
        log.warning("long timeout")
        return -1

    log.debug(f"bot with token - {token} gets update with status - {data.status_code}")

    if data.status_code == 200:
        try:
            response = Updates(**data.json())
            return response
        except ValidationError as e:
            return -1
    else:
        try:
            log.info(
                f"something wrong with bot - "
                f"{token} gets update with status - "
                f"{data.status_code} and payload - {data.json()}"
            )
        except Exception as e:
            log.info(f"can't decode json from response, error - {str(e)}")
        return -1
