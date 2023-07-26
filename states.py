from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStates(StatesGroup):
    contact = State()
    location = State()
    location2 = State()
    state1 = State()

class UserStates3(StatesGroup):
    star = State()
    review = State()