from telebot.handler_backends import State, StatesGroup


class UserChoiceState(StatesGroup):
    event_type = State()
    date = State()
    events = State()
