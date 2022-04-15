import requests
from handlers.apig_sdk import signer
from json import dumps, loads

sig = signer.Signer()
sig.Key = "***"
sig.Secret = "***"


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


send_log(log="sdfafsdaf",
         bot_name="sberauto",
         func_host="***")
