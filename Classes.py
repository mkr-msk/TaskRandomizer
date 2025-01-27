from aiogram.fsm.state import State, StatesGroup


class Element(StatesGroup):
    def __init__(self, name: str, priority: int, active: int):
        self.name = name
        self.priority = priority
        self.active = active

class AddElementState(StatesGroup):
    name = State()
    priority = State()
    active = State()

class UpdateNameState(StatesGroup):
    name = State()

class UpdatePriorityState(StatesGroup):
    priority = State()