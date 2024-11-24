from typing import TypedDict


Command = TypedDict('Command', {'input': str, 'modifiers': str, 'title': str})
CommandList = list[Command]
