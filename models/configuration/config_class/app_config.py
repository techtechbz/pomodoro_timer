from typing import Final

from custom_types.settings import AppSettings
from models.configuration.config_class.alarm_config import AlarmConfig
from models.configuration.config_class.music_player_config import MusicPlayerConfig
from models.configuration.config_class.task_recorder_config import TaskRecorderConfig
from models.configuration.config_class.timer_config import TimerConfig


class AppConfig:
    def __init__(self, preset_index_settings, timer_settings_list, alarm_settings,
                 task_recorder_settings, music_player_settings) -> None:
        self.__preset_index: int = preset_index_settings["preset_index"]
        self.__timer_config_list: Final[list[TimerConfig]] = \
            [TimerConfig(**settings) for settings in timer_settings_list]
        self.__task_recorder_config: Final[TaskRecorderConfig] = TaskRecorderConfig(**task_recorder_settings)
        self.__alarm_config: Final[AlarmConfig] = AlarmConfig(**alarm_settings)
        self.__music_player_config: Final[MusicPlayerConfig] = MusicPlayerConfig(**music_player_settings)

    def get_specified_timer_config_preset(self) -> TimerConfig:
        return self.__timer_config_list[self.__preset_index]

    def get_preset_index(self) -> int:
        return self.__preset_index

    def set_preset_index(self, preset_index: int) -> None:
        self.__preset_index = preset_index

    def get_preset_name(self) -> str:
        return self.__timer_config_list[self.__preset_index].get_preset_name()

    def get_task_recorder_config(self) -> TaskRecorderConfig:
        return self.__task_recorder_config

    def get_alarm_config(self) -> AlarmConfig:
        return self.__alarm_config

    def get_music_player_config(self) -> MusicPlayerConfig:
        return self.__music_player_config

    def get_all_settings(self) -> AppSettings:
        return {
            "preset_index_settings": {"preset_index": self.__preset_index},
            "timer_settings_list": [config.get_settings() for config in self.__timer_config_list],
            "task_recorder_settings": self.__task_recorder_config.get_settings(),
            "alarm_settings": self.__alarm_config.get_settings(),
            "music_player_settings": self.__music_player_config.get_settings()
        }
