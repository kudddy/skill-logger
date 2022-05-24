import unittest
import wrapt

from plugins.cache.storage import MemoryController


# memory = MemoryController()

# TODO add tests for update cache


def generate_data_for_memory_auth():
    return {
        "sberauto": {
            "token": "499071969:AAF6Zhvq0qD66aeRrOobrpE0bpzIStzyoN4",
            "auth": "50370344-b975-11ec-8422-0242ac120002"
        }
    }


def generate_data_for_valid_users():
    return {
        "sberauto": [
            "81432612",
            "710828013",
            "409953458",
            "421873461"
        ]
    }


def generate_data_for_users_role_model():
    return {
        "81432612": [("all",
                      "7099107585749024769",
                      "sberauto")
                     ],
        "710828013": [("all",
                       "7099122669674168321",
                       "sberauto")
                      ],
        "409953458": [("all",
                       "7099352416064765953",
                       "sberauto")
                      ],
        "421873461": [("all",
                       "7099658037347614721",
                       "sberauto")
                      ]
    }


### monkey patching for MemoryController
@wrapt.patch_function_wrapper(MemoryController, '__init__')
def new_init(wrapped, instance, args, kwargs):
    # here, wrapped is the original __init__,
    # instance is `self` instance (it is not true for classmethods though),
    # args and kwargs are tuple and dict respectively.

    # first call original init
    wrapped(*args, **kwargs)  # note it is already bound to the instance
    # and now do our changes
    instance.memory_auth = generate_data_for_memory_auth()
    instance.memory_valid_users = generate_data_for_valid_users()
    instance.memory_users_role_model = generate_data_for_users_role_model()


memory = MemoryController()


class TestMemoryController(unittest.TestCase):
    def test_get_valid_users(self):
        bot_name = "sberauto"

        valid_users = memory.get_valid_users(bot_name)

        real_valid_users = [
            "81432612",
            "710828013",
            "409953458",
            "421873461"
        ]

        self.assertEqual(valid_users, real_valid_users)

        bot_name = "test"
        valid_users = memory.get_valid_users(bot_name)

        self.assertEqual([], valid_users)

    def test_check_user(self):
        token = "499071969:AAF6Zhvq0qD66aeRrOobrpE0bpzIStzyoN4"

        auth_id = "50370344-b975-11ec-8422-0242ac120002"

        user_permission = memory.check_user(token=token, auth_uid=auth_id)

        self.assertEqual("sberauto", user_permission)

        new_token = "499071969:AAF6Zhvq0qD66aeRrOobrpE0bpzIStzyoN5"
        new_auth_id = "50370344-b975-11ec-8422-0242ac120002"

        user_permission = memory.check_user(token=new_token, auth_uid=new_auth_id)

        self.assertEqual("not_valid_user", user_permission)

    def test_check_permission_to_add_new_bot(self):
        auth_uid = "23432588358435"

        user_permission = memory.check_permission_to_add_new_bot(auth_uid=auth_uid)

        self.assertEqual(True, user_permission)

    def test_get_all_tokens(self):
        real_all_tokens = ["499071969:AAF6Zhvq0qD66aeRrOobrpE0bpzIStzyoN4"]

        all_tokens = memory.get_all_tokens()

        self.assertEqual(real_all_tokens, all_tokens)

    def test_get_bot_name_by_token(self):
        token = "499071969:AAF6Zhvq0qD66aeRrOobrpE0bpzIStzyoN4"

        bot_name = "sberauto"

        self.assertEqual(bot_name, memory.get_bot_name_by_token(token))

        token = "not_valid_token"

        self.assertEqual("", memory.get_bot_name_by_token(token))

    def test_get_token_by_bot_name(self):
        bot_name = "sberauto"
        token = "499071969:AAF6Zhvq0qD66aeRrOobrpE0bpzIStzyoN4"

        self.assertEqual(token, memory.get_token_by_bot_name(bot_name))

        self.assertEqual("", memory.get_bot_name_by_token("not_valid_token"))

    def test_user_already_subscribe(self):
        self.assertEqual(True, memory.user_already_subscribe(chat_id="81432612", bot_name="sberauto"))

        self.assertEqual(False, memory.user_already_subscribe(chat_id="not_valid_id", bot_name="sberauto"))

    def test_check_bot_exist(self):
        self.assertEqual(True, memory.check_bot_exist("sberauto"))

        self.assertEqual(False, memory.check_bot_exist("not_valid_botname"))

    def test_get_user_rule(self):
        self.assertEqual("all", memory.get_user_rule("81432612", bot_name="sberauto"))

        self.assertEqual("", memory.get_user_rule("not_valid_chat_id", bot_name="sberauto"))

    def test_get_user_id_for_update_rule(self):
        self.assertEqual("7099107585749024769",
                         memory.get_user_id_for_update_rule(chat_id="81432612",
                                                            bot_name="sberauto"))

        self.assertEqual("", memory.get_user_id_for_update_rule(
            chat_id="not_valid_token",
            bot_name="not_valid_user"
        ))
