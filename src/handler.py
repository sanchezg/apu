from datetime import datetime
import json

from src.bot import ApuBot, ApuError
from src.gsheets import SpreadsheetsManager

def apu_handler(event, context):
    print(f"## Event: {event}")
    print(f"## Context: {context}")

    bot = ApuBot()
    gsheets = SpreadsheetsManager()

    event_body: dict = json.loads(event.get("body", {}))
    try:
        bot.process_update(update_event=event_body)
    except ApuError as exc:
        print(exc.message)
        return {
            "statusCode": 200,
        }

    gsheets.authorize_credentials()
    if bot.command == "new":
        cmd_args = bot.process_command()
        gsheets.add_spending(
            s_date=bot.local_date.strftime("%d-%m-%Y"),
            s_type=cmd_args[0],
            s_category1=cmd_args[1],
            s_category2=cmd_args[2],
            s_dest=cmd_args[3],
            s_amount=int(cmd_args[4]),
            s_currency=cmd_args[5],
            exch_rate=1
        )

    bot.send_answer(message=f"Received: {bot.command}")

    return {
        "statusCode": 200
    }
