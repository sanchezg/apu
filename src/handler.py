import os
import sys

sys.path.insert(0, "src/vendor")

import requests

from .utils import parse_event


TOKEN = os.environ["TELEGRAM_TOKEN"]
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"


def send_response(text, chat_id):
    url = f"{BASE_URL}/sendMessage?text={text}&chat_id={chat_id}"
    print(f"trying to send message to {url}...")

    requests.get(url)


def apu_handler(event, context):
    print(f"## Event: {event}")
    print(f"## Context: {context}")

    try:
        command, _date, chat_id = parse_event(event)
    except Exception as exc:
        print(exc.message)
        return {
            "statusCode": 200,
        }

    send_response(f"\"command: {command}\"", chat_id)

    return {
        "statusCode": 200
    }
