from models.configuration.validator.validation_status import ValidationStatus
from models.sound.sound_effect import AlarmName


class AlarmConfigValidator:
	def __init__(self):
		self.__status = ValidationStatus.unverified
		self.__message = ""

	def validation(self, alarm_index):
		self.__status = ValidationStatus.unverified
		self.__message = ""
		try:
			_ = AlarmName(alarm_index)
			self.__status = ValidationStatus.success
			return {"alarm_index": alarm_index}
		except ValueError:
			self.__status = ValidationStatus.error
			self.__message = "・アラーム: 不正な値です。"
	
	def return_validation_result(self):
		return self.__status, self.__message
		
	def is_valid_settings(self):
		return self.__status == ValidationStatus.success
