
from prometheus_client import Summary

from ..plugins.inputer import inputter
from ..plugins.helper import timing


REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')


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


# Раскомментируйте и измените этот метод, если вам нужен кастомный HealthCheck
# def health():
#     return True, "Custom healthcheck"
