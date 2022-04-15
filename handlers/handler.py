from json import loads

import requests.auth
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from prometheus_client import Summary
from python_function_model import FunctionRequest, FunctionResponse

from ..plugins.inputer import inputter
from ..plugins.helper import timing
from ..plugins.config import setting

from .apig_sdk import signer

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
dataspace_url = setting.app.auth.url
app_key = setting.app.auth.key
app_secret = setting.app.auth.secret


# Метод handlers. Этот метод будет вызываться при вызове функции
@REQUEST_TIME.time()
@timing
def handler(request):
    payload = request.form if request.form else request.json
    resp = inputter(payload)

    return (
        resp
        ,
        200,
        {"Content-Type": "application/json"})


# Аутентификация запроса
class DataspaceAuth(requests.auth.AuthBase):
    def __call__(self, r):
        if app_key is None or app_secret is None:
            print("APP_SECRET or APP_KEY is undefined. Request will not be signed")
            return r

        sig = signer.Signer()
        sig.Key = app_key
        sig.Secret = app_secret
        request = signer.HttpRequest(r.method, r.url, r.headers, r.body.decode('utf-8'))
        sig.Sign(request)
        r.headers = request.headers
        return r


# Инициализация GraphQl клиента
if dataspace_url is not None:
    transport = RequestsHTTPTransport(url=dataspace_url, auth=DataspaceAuth(), verify=False)
    client = Client(transport=transport, fetch_schema_from_transport=False)
    graphql_status = "Dataspace URL: " + dataspace_url
else:
    client = None
    graphql_status = "DATASPACE_URL environment variable is not set. GraphQL client disabled"


# Пример вызова DataSpace с подписью
def call_dataspace():
    # Запрос
    query = gql("query ($paramId: ID!) { some_operation( id: $paramId) { some_field } }")
    variable_values = {
        "paramId": "paramValue"
    }
    # Вызов Dataspace
    return client.execute(query, variable_values=variable_values)

# Раскомментируйте и измените этот метод, если вам нужен кастомный HealthCheck
# def health():
#     return True, "Custom healthcheck"
