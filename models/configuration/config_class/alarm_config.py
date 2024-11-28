from custom_types.settings import AlarmSettings


class AlarmConfig:
	def __init__(self, alarm_index: int, will_notice: bool, notice_seconds: int) -> None:
		self.__alarm_index = alarm_index
		self.__will_notice = will_notice
		self.__notice_seconds = notice_seconds

	def get_settings(self) -> AlarmSettings:
		return {
			"alarm_index": self.__alarm_index,
			"will_notice": self.__will_notice,
			"notice_seconds": self.__notice_seconds,
		}
