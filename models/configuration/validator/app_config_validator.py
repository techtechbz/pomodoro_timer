from models.configuration.validator.validation_status import ValidationStatus
from models.configuration.validator.alarm_config_validator import AlarmConfigValidator
from models.configuration.validator.task_recorder_config_validator import TaskRecorderConfigValidator
from models.configuration.validator.timer_config_validator import TimerConfigValidator
from models.configuration.validator.music_player_config_validator import MusicPlayerConfigValidator


class AppConfigValidator:
    def __init__(self):
        self.__status = ValidationStatus.unverified
        self.__message = ""
        self.__timer_config_validator = TimerConfigValidator()
        self.__task_recorder_config_validator = TaskRecorderConfigValidator()
        self.__alarm_config_validator = AlarmConfigValidator()
        self.__music_player_config_validator = MusicPlayerConfigValidator()

    @staticmethod
    def preset_index_validation(preset_index, timer_config_inputs):
        if preset_index < 1 or preset_index > len(timer_config_inputs):
            raise ValueError('プリセットに不正な値が挿入されています。')

    def update_validation_status(self, status, message):
        if status.value > self.__status.value:
            self.__status = status
        if self.__message != "":
            self.__message += '\n'
        self.__message += message

    def tally_validation_result(self, is_valid_timer_settings, is_valid_task_recorder_settings,
                                is_valid_alarm_settings, is_valid_music_player_settings):
        if not is_valid_timer_settings:
            self.__status, self.__message = self.__timer_config_validator.return_validation_result()

        if not is_valid_alarm_settings:
            self.update_validation_status(*self.__alarm_config_validator.return_validation_result())

        if not is_valid_task_recorder_settings:
            self.update_validation_status(*self.__task_recorder_config_validator.return_validation_result())

        if not is_valid_music_player_settings:
            self.update_validation_status(*self.__music_player_config_validator.return_validation_result())

    def validation(self, preset_index_settings, timer_settings_list, task_recorder_settings,
                   alarm_settings, music_player_settings):
        self.__status = ValidationStatus.unverified
        self.__message = ""
        validated_timer_settings_list = self.__timer_config_validator.validation(timer_settings_list)
        validated_task_recorder_settings = self.__task_recorder_config_validator.validation(**task_recorder_settings)
        validated_alarm_settings = self.__alarm_config_validator.validation(**alarm_settings)
        validated_music_player_settings = self.__music_player_config_validator.validation(**music_player_settings)

        self.tally_validation_result(
            self.__timer_config_validator.is_valid_settings(),
            self.__task_recorder_config_validator.is_valid_settings(),
            self.__alarm_config_validator.is_valid_settings(),
            self.__music_player_config_validator.is_valid_settings())

        if self.__status == ValidationStatus.unverified:
            self.__status = ValidationStatus.success

        return {
            "preset_index_settings": preset_index_settings,
            "timer_settings_list": validated_timer_settings_list,
            "task_recorder_settings": validated_task_recorder_settings,
            "alarm_settings": validated_alarm_settings,
            "music_player_settings": validated_music_player_settings
        }

    def return_validation_status(self):
        return self.__status

    def return_validation_message(self):
        return self.__message
