class InvalidUserError(Exception):
    message = "Sorry, I don't know you (ref: invalid-user)."


class InvalidMessageError(Exception):
    message = "Sorry, I don't understand you (ref: invalid-command)."


class InvalidEventError(Exception):
    message = "Sorry, I can't do nothing with that (ref: invalid-event)."
