from enum import Enum, auto
from typing import Final


class CommandCategory(Enum):
    timer = auto()
    config = auto()
    task = auto()
    alert = auto()
    dialog = auto()
    preset = auto()


class KeyCommand:
    def __init__(self) -> None:
        self.__key_commands_list: Final[list[dict[str, str]]] = [
            # timer
            {'input': 'P', 'modifiers': 'cmd', 'title': 'play'},
            {'input': '\b', 'modifiers': 'cmd', 'title': 'clear'},
            # config
            {'input': 'M', 'modifiers': 'cmd', 'title': 'music'},
            {'input': 'I', 'modifiers': 'cmd', 'title': 'config'},
            # task
            {'input': 'T', 'modifiers': 'cmd', 'title': 'task'},
            # alert
            {'input': 'C', 'modifiers': 'cmd', 'title': 'interrupt'},
            {'input': '\r', 'modifiers': 'cmd', 'title': 'confirm'},
            # dialog
            {'input': 'D', 'modifiers': 'cmd', 'title': 'default'},
            {'input': 'S', 'modifiers': 'cmd', 'title': 'save'},
            # change preset
            {'input': '1', 'modifiers': 'cmd', 'title': 'preset'},
            {'input': '2', 'modifiers': 'cmd', 'title': 'preset'},
            {'input': '3', 'modifiers': 'cmd', 'title': 'preset'},
            {'input': '4', 'modifiers': 'cmd', 'title': 'preset'},
            {'input': '5', 'modifiers': 'cmd', 'title': 'preset'},
        ]

    def get_key_commands_list(self) -> list[dict[str, str]]:
        return self.__key_commands_list

    @staticmethod
    def categorize_command(sender) -> CommandCategory:
        if sender['title'] in ('play', 'clear'):
            return CommandCategory.timer
        if sender['title'] in ('music', 'config'):
            return CommandCategory.config
        if sender['title'] == 'task':
            return CommandCategory.task
        if sender['title'] in ('default', 'save'):
            return CommandCategory.dialog
        if sender['title'] == 'preset':
            return CommandCategory.preset
        return CommandCategory.alert
