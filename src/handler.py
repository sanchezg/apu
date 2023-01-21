import json

from src.bot import ApuBot, ApuError

def apu_handler(event, context):
    print(f"## Event: {event}")
    print(f"## Context: {context}")

    bot = ApuBot()

    event_body: dict = json.loads(event.get("body", {}))
    try:
        bot.process_update(update_event=event_body)
    except ApuError as exc:
        print(exc.message)
        return {
            "statusCode": 200,
        }

    bot.send_answer(message=f"Received: {bot.command}")

    return {
        "statusCode": 200
    }
