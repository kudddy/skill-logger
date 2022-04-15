from pydantic import BaseModel, Field
from typing import List

example_request = {
    "MESSAGE_NAME": "LOGGER_INFO",
    "DATA": {
        "log_info": "RP123| 14.08.2022 15:00| 200",
        "bot_type": "sberauto"
    }
}


# input message
class Data(BaseModel):
    log_info: str
    bot_type: str
    consumer_ids: List[int] = None


class Request(BaseModel):
    MESSAGE_NAME: str
    DATA: Data


# update answer from tlg
class From(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    username: str or None = None
    language_code: str = None


class Chat(BaseModel):
    id: int
    first_name: str
    username: str or None = None
    type: str


class Photo(BaseModel):
    file_id: str
    file_unique_id: str
    file_size: int
    width: int
    height: int


class InlineKeyboard(BaseModel):
    text: str
    callback_data: str or None = None
    url: str or None = None


class ReplyMarkup(BaseModel):
    inline_keyboard: List[List[InlineKeyboard]]


class Message(BaseModel):
    message_id: int
    frm: From = Field(..., alias='from')
    chat: Chat
    photo: List[Photo] = None
    date: int
    edit_date: int = None
    text: str = None
    reply_markup: ReplyMarkup = None


class Updater(BaseModel):
    update_id: int
    message: Message = None


class Updates(BaseModel):
    ok: bool
    result: List[Updater]
