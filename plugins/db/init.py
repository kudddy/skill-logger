import requests.auth
from gql import Client
from gql.transport.requests import RequestsHTTPTransport

# try:
from ..config import setting
from .apig_sdk import signer
# except Exception as e:
#     from plugins.config import setting
#     from plugins.db.apig_sdk import signer

dataspace_url = setting.app.auth.url
app_key = setting.app.auth.key
app_secret = setting.app.auth.secret


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
if setting.app.main.use_graph_ql:
    if dataspace_url is not None:
        transport = RequestsHTTPTransport(url=dataspace_url, auth=DataspaceAuth(), verify=False)
        client = Client(transport=transport, fetch_schema_from_transport=False)
        graphql_status = "Dataspace URL: " + dataspace_url
    else:
        client = None
        graphql_status = "DATASPACE_URL environment variable is not set. GraphQL client disabled"
    print(graphql_status)
else:
    print("We don't use graphql")
