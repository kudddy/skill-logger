from gql import gql

from ..db.init import client


def insert_valid_user(bot_name: str, chat_id: str):
    query = gql("""mutation ($botName: String!, $chatId: String!){
      p1: packet {
        createLogValidUser(input: {
          botName: $botName,
          chatId: $chatId,
        }){
          chatId
        }
      }
    }""")
    variable_values = {
        "botName": bot_name,
        "chatId": chat_id
    }
    return client.execute(query, variable_values=variable_values)


def insert_log_auth_data(tlg_token: str, auth_token: str, bot_name: str):
    query = gql("""mutation ($botName: String!, $tlgToken: String!, $authToken: String!){
      p1: packet {
        createLogAuthData(input: {
          botName: $botName,
          tlgToken: $tlgToken,
          authToken: $authToken
          
        }){
          botName
        }
      }
    }""")
    variable_values = {
        "botName": bot_name,
        "tlgToken": tlg_token,
        "authToken": auth_token
    }
    return client.execute(query, variable_values=variable_values)


def get_auth_data():
    query = gql("""query {
      searchLogAuthData{
        elems {
          tlgToken,
          authToken,
          botName
        }
      }
    }""")
    return client.execute(query)


def get_valid_users():
    query = gql("""query {
      searchLogValidUser{
        elems {
          chatId,
          botName
        }
      }
    }""")
    return client.execute(query)


def get_rule_model_data():
    query = gql("""query {
      searchLogValidUser{
        elems {
          id,
          botName,
          chatId,
          ruleType
        }
      }
    }""")
    return client.execute(query)


def update_rule_model_data(id_: str, chat_id: str, rule_type: str):
    query = gql("""mutation ($id: ID!, $chatId: String!, $ruleType: String!){
      p1: packet {
        updateLogValidUser(input: {
          id: $id,
          chatId: $chatId,
          ruleType: $ruleType
        }){
          id
        }
      }
    }""")
    variable_values = {
        "id": id_,
        "chatId": chat_id,
        "ruleType": rule_type
    }

    return client.execute(query, variable_values=variable_values).get("p1", {})\
        .get("updateLogValidUser", {}).get("id", "")
