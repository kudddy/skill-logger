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

### Как достучаться к сервису с помощью python клиента?
https://github.com/kudddy/ApiGateway-python-sdk-2.0.4 - пример с кодом

Описание:
request payload:
```
{
    "MESSAGE_NAME": "LOGGER_INFO",
    "DATA": {
        "log_info": "RP123| 14.08.2022 15:00| 200", \\ формат лога
        "bot_type": "df" \\ тип бота 
    }
}

```
response payload:
```
{
    "CODE": 404, \\ code error
    "DATA": {
        "desc": "something, bot - df is not exist." \\ error description
    },
    "MESSAGE_NAME": "LOGGER_INFO", \\ static message name
    "STATUS": false \\ global response time
}
```

### Механика работы сервиса

#### Регистрация нового бота для навыка 


1. Сначала требуется создать нового бота в TLG используя BotFather, нам понадобится токен

2. Переходим в https://t.me/sberAutoLogger_bot для регистрации бота

3. Формируем строку - ```3234234234[auth_uid] | sberlog[botname] | 432424124[bot_token] | 863782568325[new_auth_token] | register```, 
где первый параметр - это аутентификационный uid(выдается адмимистратором),  второй - читаемое название бота латиницей, третий - токен, который нам дал bot_father,  
четвертый -  новый аутентификационный токен для валидации пользователей(любая строка), потребуется для дальнейшей аутентификиции, пятый - тип действия

4. Если все ок,  то бот ответ сообщением что процедура прошла успешно. 

5. Переходим в созданного дата и отправляем сообщение формата - ```43234234234[new_auth_token] | subscription```, где new_auth_token - значение их предыдущего шага

6. Бот пишет что все ок тем самым подписывет вас на обновления

7. PROFIT...

