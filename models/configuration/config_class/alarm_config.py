from custom_types.settings import AlarmSettings


class AlarmConfig:
	def __init__(self, alarm_index: int) -> None:
		self.__alarm_index = alarm_index

	def get_settings(self) -> AlarmSettings:
		return {"alarm_index": self.__alarm_index}
