from datetime import datetime, timezone, timedelta
import json
import os
import sys
sys.path.insert(0, "src/vendor")

import requests

TOKEN = os.environ["TELEGRAM_TOKEN"]
USER_ID = os.environ["TELEGRAM_USER_ID"]
ART = timezone(-timedelta(hours=3))


class ApuError(Exception):
    def __init__(self, message, *args: object) -> None:
        self.message = message
        super().__init__(*args)


class ApuBot:
    AVAILABLE_COMMANDS = ["new", "list"]

    def __init__(self, token: str = TOKEN, user_id: str = USER_ID, tz: timezone = ART) -> None:
        self._token = token
        self._user_id = user_id
        self._base_url = f"https://api.telegram.org/bot{self._token}"
        self._update_event: dict = None  # TODO: move update to a dataclass object
        self.date: datetime = None
        self.local_date: datetime = None
        self.tz = tz

    def validate_message(self, update: dict):
        """
        Validates the input message.
        TODO: move to a validation method into a Message dataclass.
        """
        if self._user_id and any(("from" in update, "chat" in update)):
            from_user = update.get("from", update["chat"]).get("id", 9999)  # just a random number to missmatch
            if str(from_user) != str(self._user_id):
                print(f"User error: {from_user} and {self._user_id}")
                raise ApuError(message="Sorry, I don't know you (ref: invalid-user).")

        text: str = update.get("text", "")
        if not any(
            [
                text.startswith("/new"),
                text.startswith("/list"),
            ]
        ):
            raise ApuError(message="Sorry, I don't understand you (ref: invalid-command).")

    def parse_command(self, command_text: str):
        command_args = command_text[1:].split(maxsplit=1)
        return command_args[0], command_args[1:]  # if no args, then split returns just the command

    def process_update(self, update_event: dict):
        """
        Process the input data incoming from Telegram API webhook.
        Input data must follows Update object format: https://core.telegram.org/bots/api#update
        """
        self._update_event = update_event

        if "message" in update_event:
            self._process_message()
        elif "callback_query" in update_event:
            self._process_callback_query()
        else:
            # TODO: move to a validation method into Update dataclass
            raise ApuError(message="Sorry, I can't do nothing with that (ref: invalid-event).")

    def _process_message(self):
        message = self._update_event["message"]
        self.validate_message(message)
        self.command, self.command_args = self.parse_command(message["text"])
        if self.command_args:
            self.command_args = [x for x in self.command_args[0].split()]

        self.date: datetime = datetime.fromtimestamp(message["date"], timezone.utc)
        self.local_date: datetime = datetime.fromtimestamp(message["date"], timezone.utc).astimezone(tz=self.tz)
        self.chat_id = message["chat"]["id"]

    def _process_callback_query(self):
        callback_query = self._update_event["callback_query"]
        message = callback_query["message"]
        self.date: datetime = datetime.fromtimestamp(message["date"], timezone.utc)
        self.local_date: self.date.astimezone(self.tz)
        self.chat_id = message["chat"]["id"]

        chosen_option: str = callback_query["data"]  # TODO
        if chosen_option.startswith("categoria1"):
            pass
        elif chosen_option.startswith("categoria2"):
            pass
        elif chosen_option.startswith("destinatario"):
            pass
        elif chosen_option.startswith("cantidad"):
            pass
        elif chosen_option.startswith("moneda"):
            pass
        else:
            pass

    def process_new(self):
        if not self.command_args:
            print("## No arguments, sending inlineKeyboard to the user")
            self.send_api_command(
                "sendMessage",
                text="Elegir categoria 1 del gasto",
                chat_id=self.chat_id,
                reply_markup=json.dumps(
                    {
                        "inline_keyboard": [
                            [{"text": "Mano de obra", "callback_data": "mano_de_obra"}],
                            [{"text": "Administracion", "callback_data": "administracion"}],
                            [{"text": "Materiales", "callback_data": "materiales"}],
                            [{"text": "Insumos", "callback_data": "insumos"}]
                        ]
                    }
                )
            )
            return

        return self.command_args

    def process_list(self):
        pass

    def process_command(self):
        process_methods = {
            x: getattr(self, f"process_{x}") for x in self.AVAILABLE_COMMANDS
        }
        return process_methods[self.command]()

    def send_api_command(self, command, **kwargs):
        url = f"{self._base_url}/{command}"
        response = requests.get(url, params=kwargs)
        print(f"## Send message to user, response: {response} | {response.content}")

    def send_answer(self, message: str):
        self.send_api_command("sendMessage", text=message, chat_id=self.chat_id)
