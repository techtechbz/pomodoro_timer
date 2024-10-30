from typing import Final, Optional

from models.configuration.validator.validation_status import ValidationStatus
from models.configuration.config_class.app_config import AppConfig
from models.configuration.ini_file_parser import IniFileParser
from models.configuration.validator.app_config_validator import AppConfigValidator


class ConfigProvider:
	def __init__(self):
		self.__alert_message = ""
		self.__validator: Final[AppConfigValidator] = AppConfigValidator()
		self.__ini_file_parser: Final[IniFileParser] = IniFileParser()
	
	def get_alert_message(self) -> str:
		return self.__alert_message
	
	def validate_settings(self, settings):
		validated_settings = self.__validator.validation(**settings)
		status = self.__validator.return_validation_status()
		message = self.__validator.return_validation_message()
		if status == ValidationStatus.error:
			self.__alert_message = message
			validated_settings = None
		return validated_settings, status, message
	
	def get_saved_config(self) -> Optional[AppConfig]:
		saved_settings = self.__ini_file_parser.get_saved_settings()
		validated_settings, _, _ = self.validate_settings(saved_settings)
		if validated_settings is None:
			return None
		return AppConfig(**validated_settings)
	
	def save_input_settings(self, inputs) -> Optional[AppConfig]:
		self.__alert_message = ""
		validated_settings, status, message = self.validate_settings(inputs)
		if validated_settings is None:
			return None

		self.__ini_file_parser.save_changed_settings(**inputs)
		if status == ValidationStatus.success:
			self.__alert_message = "設定が保存されました!"
		elif status == ValidationStatus.warning:
			self.__alert_message = message

		return AppConfig(**validated_settings)

	def replace_config(self, config: AppConfig):
		settings = config.get_all_settings()
		self.__ini_file_parser.save_changed_settings(**settings)
