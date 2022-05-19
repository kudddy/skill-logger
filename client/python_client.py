import requests

from time import sleep
from json import dumps

from plugins.signer import HttpRequest, Signer


sig = Signer()
sig.Key = "*"
sig.Secret = "*"


def send_log(log: str, bot_name: str, func_host: str):
    body = {
        "MESSAGE_NAME": "LOGGER_INFO",
        "DATA": {
            "log_info": log,
            "bot_type": bot_name,
            "error_status": False
        }
    }

    r = HttpRequest("POST",
                    func_host,
                    {"Content-Type": "application/json", "x-stage": "RELEASE"},
                    body=dumps(body))
    sig.Sign(r)

    data = requests.request(r.method, r.scheme + "://" + r.host + r.uri, headers=r.headers, data=r.body, verify=False)

    print(data.json())


# while True:

send_log(log="RP123| 14.08.2022 15:00| 200",
         bot_name="sberauto",
         func_host="https://smapi.pv-api.sbc.space/fn_e3826261_648c_4b43_8b25_b74c1435ba0d")

