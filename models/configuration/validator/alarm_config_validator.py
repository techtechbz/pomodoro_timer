from custom_types.settings import AlarmSettings
from models.configuration.validator.validation_status import ValidationStatus
from models.sound.sound_effect import AlarmName


class AlarmConfigValidator:
	def __init__(self):
		self.__status: ValidationStatus = ValidationStatus.unverified
		self.__message: str = ""

	def alarm_index_validator(self, alarm_index: int) -> None:
		try:
			_ = AlarmName(alarm_index)
			self.__status = ValidationStatus.success
		except ValueError:
			self.__status = ValidationStatus.error
			self.__message = "・アラーム: 不正な値です。"

	def notice_seconds_validator(self, will_notice: bool, notice_seconds: str) -> int:
		if not will_notice:
			return 0
		max_value = 300
		try:
			value = int(notice_seconds)
			if not all((value >= 1, value <= max_value)):
				raise ValueError()
			return value
		except ValueError:
			self.__status = ValidationStatus.error
			if self.__message != "":
				self.__message += "\n"
			self.__message += f'・通知する秒数(秒前): 1~{max_value}までの数字で指定してください。'

	def validation(self, alarm_index: int, will_notice: bool, notice_seconds: str) -> AlarmSettings:
		self.__status = ValidationStatus.unverified
		self.__message = ""

		self.alarm_index_validator(alarm_index)
		validated_notice_seconds = self.notice_seconds_validator(will_notice, notice_seconds)

		return {"alarm_index": alarm_index, 'will_notice': will_notice, 'notice_seconds': validated_notice_seconds}
	
	def return_validation_result(self) -> tuple[ValidationStatus, str]:
		return self.__status, self.__message

	def is_valid_settings(self) -> bool:
		return self.__status == ValidationStatus.success
