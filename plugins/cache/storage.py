from typing import List
from time import time
from ..db.query import get_auth_data, get_valid_users, get_rule_model_data
from ..config import setting

# memory_auth = {
#     "sberauto": {
#         "token": "****",
#         "auth": "****"
#     },
#     "lolo": {
#         "token": "*****",
#         "auth": "*****"
#     }
# }

# memory_map = {
#     "sberauto": [123412, 432542345, 432532453425],
#     "lolo": [234124, 23412342314, 213421342134]
#
# }

memory_user_rule_model = {
    432542345: ("all", 435131251235, 'sberauto')
}

rule_model = "only_errors"


class MemoryController:
    def __init__(self):
        self.memory_auth = self._init_cache_memory_auth()
        self.memory_valid_users = self._init_cache_memory_valid_user()
        self.memory_users_role_model = self._init_cache_memory_rule_model()

        self._init_time = time()

    def update_memory_users_role_model(self):
        self.memory_users_role_model = self._init_cache_memory_rule_model()

    def _update_cache(self):
        if time() - self._init_time > setting.app.main.update_cache_every:
            self._init_time = time()

            self.memory_auth = self._init_cache_memory_auth()
            self.memory_valid_users = self._init_cache_memory_valid_user()
            self.memory_rule_model = self._init_cache_memory_rule_model()

    @staticmethod
    def _init_cache_memory_auth():
        memory_auth = get_auth_data()

        return {
            k.get("botName"): {"token": k.get("tlgToken"), "auth": k.get("authToken")} for k in
            memory_auth.get("searchLogAuthData").get("elems")
        }

    @staticmethod
    def _init_cache_memory_rule_model():

        memory_rule_model = get_rule_model_data()

        data = memory_rule_model.get("searchLogValidUser").get("elems")

        struct_data = {}

        for v in data:
            if v.get("chatId") in struct_data:
                struct_data[v.get("chatId")].append((v.get("ruleType"), v.get("id"), v.get("botName")))
            else:
                struct_data[v.get("chatId")] = [(v.get("ruleType"), v.get("id"), v.get("botName"))]

        return struct_data

    @staticmethod
    def _init_cache_memory_valid_user():
        valid_users = get_valid_users()
        normalized_valid_users = {}
        for d in valid_users.get("searchLogValidUser").get("elems"):
            if d.get("botName") in normalized_valid_users:
                if not d.get("chatId") in normalized_valid_users[d.get("botName")]:
                    normalized_valid_users[d.get("botName")].append(d.get("chatId"))
            else:
                normalized_valid_users[d.get("botName")] = [d.get("chatId")]

        return normalized_valid_users

    def check_user(self, token: str, auth_uid: str) -> str:

        self._update_cache()

        for bot_name, v in self.memory_auth.items():
            if v.get("token") == token and v.get("auth") == auth_uid:
                return bot_name

        return "not_valid_user"

    def check_permission_to_add_new_bot(self, auth_uid: str) -> bool:

        self._update_cache()

        # TODO for all bots one token, it is not true
        if auth_uid == setting.app.auth.token_for_reg_bots:
            return True
        return False

    def get_valid_users(self, bot_name: str) -> list:
        return self.memory_valid_users.get(bot_name, [])

    def get_all_tokens(self) -> List[str]:
        all_tokens = []
        for k, v in self.memory_auth.items():
            all_tokens.append(v.get("token"))
        return all_tokens

    def get_bot_name_by_token(self, token: str):

        for k, v in self.memory_auth.items():
            if v.get("token") == token:
                return k

        return ""

    def update_cache_with_valid_users(self, chat_id: int, bot_name: str):

        if bot_name in self.memory_valid_users:
            self.memory_valid_users[bot_name].append(str(chat_id))
        else:
            self.memory_valid_users[bot_name] = [str(chat_id)]

    def update_memory_auth_cache(self, tlg_token: str, auth_token: str, bot_name: str):

        self.memory_auth.update({
            bot_name: {
                "token": tlg_token,
                "auth": auth_token
            }
        })

    def get_token_by_bot_name(self, bot_name: str) -> str:
        return self.memory_auth.get(bot_name, {}).get("token", "")

    def user_already_subscribe(self, bot_name: str, chat_id: str):
        if str(chat_id) in self.memory_valid_users.get(bot_name, []):
            return True
        return False

    def check_bot_exist(self, bot_name: str):
        if bot_name in self.memory_auth:
            return True
        return False

    def get_user_rule(self, chat_id: str, bot_name: str) -> str:
        for data in self.memory_users_role_model.get(chat_id):
            if bot_name == data[2]:
                return data[0]
        return ""

    def get_user_id_for_update_rule(self, chat_id: str, bot_name: str):
        for data in self.memory_users_role_model.get(chat_id):
            if data[2] == bot_name:
                return data[1]
        return ""

    def update_memory_user_rule(self, chat_id: str, rule: str, id_: str, bot_name: str):
        data = self.memory_users_role_model.get(chat_id)

        for k, v in enumerate(data):
            if bot_name == v[2]:
                data.pop(k)
                data.append((rule, id_, bot_name,))

        self.memory_users_role_model[chat_id] = data


memory = MemoryController()
