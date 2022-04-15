## Шаблон: python38-graphql

```
Python 3.8.6 
pip 19.3.1
```
Для корректной работы в функции должен быть скрипт `handler/handler.py` с функцией `handle` принимающей на вход `FunctionRequest` и возвращающий `FunctionResponse`.  
В `FunctionsRequest` содержится `payload`(пришедший запрос) и `headers`(заголовки).  
Дополнительная информация (path, queryParams, Content-Type и т.д.) содержатся в заголовках.  
В `FunctionsResponse` можно передать тело ответа, статус и заголовки.  

Для мониторинга метрик используется библиотека [prometheus/client_python](https://github.com/prometheus/client_python).  
Пример регистрации метрики можно увидеть в [`handler.py`](handlers/handler.py).

### Подключение внешних зависимостей
Внешние зависимости могут быть определены в [`requirements.txt`](./requirements.txt) проекта функции.

### Взаимодействие с DATASPACE
⚠️ **При запуске должны быть определены переменные среды DATASPACE_URL, APP_KEY, APP_SECRET** ⚠️

Dataspace поддерживает взаимодействие по протоколу GraphQL. Поэтому для вызова в данном шаблоне используется библиотека [gql](https://github.com/graphql-python/gql)

Вызовы DataSpace, идущие через API-Gateway, должны быть подписаны ключом (APP_KEY) и секретом (APP_SECRET) из переменных среды.  
Для этого используется [signer.py](handlers/apig_sdk/signer.py).  

В [`apolloClient`](handlers/handler.py) создается клиент `client` настроенный на DATASPACE_URL.  
Через него можно вызывать сервис Dataspace, выполнять различные операции - query, mutate и т.д.  
Запросы проходящие через этого клиента подписываются классом `DataspaceAuth`.

Пример подписи и вызова Dataspace можно увидеть в [handler.py](handlers/handler.py)

### Конфигурирование через ConfigMap:
Для возможности конфигурирования функции через ConfigMap пользователю необходимо:
1) Определить свойства в файле, например: `properties.ini`
2) В ```functions.yaml``` указать конфигурационные файлы для монтирования.
```yaml
    configs:
      - name: python38-graphql-example              # Имя конфигурации. В UI OSE ConfigMap будет называться <имя-функции>-cm-<имя конфигурации>
        files:                                # Список файлов для монтирования
          - properties.ini    # Полный путь до файла относительно директории с функцией
```
Данный файл будет смонтирован в папку `/app/config`.  
Далее в функции можете использовать этот файл, например через библиотеку [configparser](https://docs.python.org/3/library/configparser.html)

### Тестирование
⚠️ Этот функционал пока не работает
⚠️ **При сборке функции будет запущен скрипт [`./handler_tests.py`](./test_handler.py). Если тесты не пройдут, то функция не развернется.** ⚠️

### Как достучаться к сервису с помощью python клиента?
https://github.com/kudddy/ApiGateway-python-sdk-2.0.4 - пример с кодом

MESSAGE_NAME - имя ссобщения
text - разложенная на токены  словосочетание
new_search_engine - использовать поисковой движок?

Описание:
request payload:
```
{
    "MESSAGE_NAME": "GET_DUCKLING_RESULT",
    "data": {
        "new_search_engine": true,
        "text": [
            {
                "text": "BMW",
                "raw_text": "BMW",
                "grammem_info": {
                    "raw_gram_info": "",
                    "part_of_speech": "X"
                },
                "lemma": "bmw",
                "is_stop_word": false,
                "list_of_dependents": [],
                "dependency_type": "nsubj",
                "head": 2
            },
            {
                "text": "3",
                "raw_text": "3",
                "lemma": "3",
                "original_text": "3",
                "token_type": "NUM_TOKEN",
                "token_value": {
                    "value": 3,
                    "adjectival_number": false
                },
                "list_of_token_types_data": [
                    {
                        "token_type": "NUM_TOKEN",
                        "token_value": {
                            "value": 3,
                            "adjectival_number": false
                        }
                    }
                ],
                "grammem_info": {
                    "numform": "digit",
                    "raw_gram_info": "numform=digit",
                    "part_of_speech": "NUM"
                },
                "is_stop_word": false,
                "list_of_dependents": [
                    1
                ],
                "dependency_type": "root",
                "head": 0
            },
            {
                "raw_text": ".",
                "text": ".",
                "lemma": ".",
                "token_type": "SENTENCE_ENDPOINT_TOKEN",
                "token_value": {
                    "value": "."
                },
                "list_of_token_types_data": [
                    {
                        "token_type": "SENTENCE_ENDPOINT_TOKEN",
                        "token_value": {
                            "value": "."
                        }
                    }
                ]
            }
        ],
        "query": "BMW 3",
        "sessionid": "d702a8ff-35f0-33fb-9c86-f6879d3b463d",
        "userid": "0764AD3A-AB70-4974-BEF9-B6AEEBA51866"
    }
}
```
response payload:
```
{
    "CODE": 200,
    "MESSAGE_NAME": "GET_DUCKLING_RESULT",
    "PAYLOAD": {
        "description": "OK",
        "result": {
            "count": 194,
            "max_price": 5882700,
            "median": 2785000,
            "min_price": 200000,
            "search_keys": {
                "brand_id": 48,
                "city_id": null,
                "model_id": 591,
                "price_from": null,
                "price_to": null,
                "year_from": null,
                "year_to": null
            },
            "search_text_form": "BMW 3ER",
            "url": "https://sberauto.onelink.me/RBOE/applisting?catalog=%5B%7B%22brand_id%22%3A48%2C%22model_id%22%3A%5B591%5D%7D%5D"
        }
    },
    "STATUS": true
}
```

Типовые запросы к базе данных с использованием graphql

запись в базу
```
# mutation {
#   p1: packet {
#     createLogData(input: {
#       text: "lolka",
#       sessionId: "sdfsdfsdfdsf",
#       userId: "324dsfasdf"
#     }){
#       text
#     }
#   }
# }
```

чтение из базы с условием where
```
query {
  searchLogData(cond:"it.text=='тойота'"){
    elems {
      text,
      sessionId,
      userId,
      time
    }
  }
}
```


# тестовый план 

Регистрация бота

1. регистрация нового бота (нужна проверка на кол-во регистрируемых ботов)
```3234234234[auth_uid] | sberlog[botname] | 432424124[bot_token] | 863782568325[new_auth_token] |register``` - это можно сделать в любом боте(100% нужен аудит пользователь)
первый параметр это аутентификационный uid,  второй - читаемое название бота, третий - название токена,  
четвертый новый аутентификационный токен, пятый - тип действия```

2. Переход в бота, который создали


3. Подписались на получение обновление командой 

```43234234234 | subscription```, где первый параметр аутентификационнй для бота, а второй - тип действия

Требуется написать клиент для js и python

4. отправить запрос в сервис с логом
