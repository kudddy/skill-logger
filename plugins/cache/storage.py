from typing import List

from ..db.query import get_auth_data, get_valid_users


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


class MemoryController:
    def __init__(self):
        self.memory_auth = self._init_cache_memory_auth()
        self.memory_valid_users = self._init_cache_memory_valid_user()

    @staticmethod
    def _init_cache_memory_auth():
        memory_auth = get_auth_data()

        return {
            k.get("botName"): {"token": k.get("tlgToken"), "auth": k.get("authToken")} for k in
            memory_auth.get("searchLogAuthData").get("elems")
        }

    @staticmethod
    def _init_cache_memory_valid_user():
        valid_users = get_valid_users()

        normalized_valid_users = {}
        for d in valid_users.get("searchLogValidUser").get("elems"):
            if d.get("botName") in normalized_valid_users:
                normalized_valid_users[d.get("botName")].append(d.get("chatId"))
            else:
                normalized_valid_users[d.get("botName")] = [d.get("chatId")]

        return normalized_valid_users

    def check_user(self, token: str, auth_uid: str) -> str:

        for bot_name, v in self.memory_auth.items():
            if v.get("token") == token and v.get("auth") == auth_uid:
                return bot_name

        return "not_valid_user"

    @staticmethod
    def check_permission_to_add_new_bot(auth_uid: str) -> bool:
        # TODO we need more secure check pass
        if auth_uid == "23432588358435":
            return True

        return False

    def get_valid_users(self, bot_name: str) -> list:
        return self.memory_valid_users.get(bot_name, [])

    def get_all_tokens(self) -> List[str]:
        all_tokens = []
        for k, v in self.memory_auth.items():
            all_tokens.append(v.get("token"))
        return all_tokens

    def update_cache_with_valid_users(self, chat_id: int, bot_name: str):
        if bot_name in self.memory_valid_users:
            self.memory_valid_users[bot_name].append(chat_id)
        else:
            self.memory_valid_users[bot_name] = [chat_id]

    def get_token_by_bot_name(self, bot_name: str) -> str:
        return self.memory_auth.get(bot_name, {}).get("token", "")

    def user_already_subscribe(self, bot_name: str, chat_id: str):
        if chat_id in self.memory_valid_users.get(bot_name, []):
            return True
        return False

    def check_bot_exist(self, bot_name: str):
        if bot_name in self.memory_auth:
            return True
        return False


memory = MemoryController()
