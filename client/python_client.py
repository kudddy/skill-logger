import requests
from handlers.apig_sdk import signer
from json import dumps, loads

sig = signer.Signer()
sig.Key = "21fbb619dece43deb1c80b3280a54f6c"
sig.Secret = "94a2d93bfb7a4cb4bfcc4bf31b1f37a1"


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

    print(data.status_code, data.reason)
    print(data.content)

    print(loads(data.content))


send_log(log="sdfafsdaf",
         bot_name="sberauto",
         func_host="https://smapi.pv-api.sbc.space/fn_df4f75ea_c184_4999_92ae_5f0f20ec9f2b")
