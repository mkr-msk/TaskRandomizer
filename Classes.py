from aiogram.fsm.state import State


class Element:
    def __init__(self, name: str, priority: int, active: int):
        self.name = name
        self.priority = priority
        self.active = active

class AddElementState:
    name = State()
    priority = State()
    active = State()

class UpdateNameState:
    name = State()

class UpdatePriorityState:
    priority = State()