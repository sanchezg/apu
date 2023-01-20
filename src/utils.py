import json
import os

from .exceptions import InvalidUserError, InvalidMessageError, InvalidEventError

USER_ID = os.environ["TELEGRAM_USER_ID"]


def validate_message(message: dict):
    if USER_ID and any(("from" in message, "chat" in message)):
        from_user = message.get("from", message["chat"]).get("id", 9999)  # just a random number to missmatch
        if str(from_user) != str(USER_ID):
            print(f"User error: {from_user} and {USER_ID}")
            raise InvalidUserError()
    
    text: str = message.get("text")
    if not any(
        [
            text.startswith("/new"),
            text.startswith("/list"),
        ]
    ):
        raise InvalidMessageError()


def parse_event(event: dict):
    event_body: dict = json.loads(event.get("body", {}))
    if event_body and "message" in event_body:
        message = event_body["message"]
        validate_message(message)
        command = message["text"]
        _date = message["date"]
        chat_id = message["chat"]["id"]
        return command, _date, chat_id
    raise InvalidEventError()
