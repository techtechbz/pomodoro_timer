from enum import Enum, auto


class ValidationStatus(Enum):
	success = auto()
	unverified = auto()
	warning = auto()
	error = auto()

