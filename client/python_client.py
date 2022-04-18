import requests
from handlers.apig_sdk import signer
from json import dumps

sig = signer.Signer()
sig.Key = "*"
sig.Secret = "*"


def send_log(log: str, bot_name: str, func_host: str):
    body = {
        "MESSAGE_NAME": "LOGGER_INFO",
        "DATA": {
            "log_info": log,
            "bot_type": bot_name
        }
    }

    r = signer.HttpRequest("POST",
                           func_host,
                           {"Content-Type": "application/json", "x-stage": "RELEASE"},
                           body=dumps(body))
    sig.Sign(r)

    data = requests.request(r.method, r.scheme + "://" + r.host + r.uri, headers=r.headers, data=r.body, verify=False)


from time import sleep

while True:
    send_log(log="sdfafsdaf",
             bot_name="sberauto",
             func_host="https://smapi.pv-api.sbc.space/fn_df4f75ea_c184_4999_92ae_5f0f20ec9f2b")

    sleep(1)
