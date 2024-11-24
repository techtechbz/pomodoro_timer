import configparser
import os
from typing import Final

from custom_types.settings import AlarmSettings, AppSettings, MusicPlayerSettings, PresetSettings,\
    TaskRecorderSettings, TimerSettings
from models.configuration.default_settings import DefaultSettings


class IniFileParser:
    def __init__(self) -> None:
        self.__default_settings: Final[DefaultSettings] = DefaultSettings()
        self.__timer_preset_config_section: Final[str] = "TIMER_PRESET"
        self.__task_recorder_config_section: Final[str] = "TASK_RECORDER"
        self.__alarm_config_section: Final[str] = "ALARM"
        self.__music_player_config_section: Final[str] = "MUSIC"
        self.__ini_file_path: Final[str] = "local_config.ini"
        self.__encoder: Final[str] = "UTF-8"
        self.__configparser = configparser.ConfigParser()

        if os.path.isfile(self.__ini_file_path):
            self.__configparser.read(self.__ini_file_path, encoding=self.__encoder)
        else:
            self.set_default()
            self.save()

    def set_default(self) -> None:
        default_settings = self.__default_settings.get_default_settings()
        self.__configparser[self.__timer_preset_config_section] = default_settings["preset_index_settings"]
        for i in range(self.__default_settings.get_total_preset_number()):
            self.__configparser[self.get_preset_section(i)] = default_settings["timer_settings_list"][i]
        self.__configparser[self.__task_recorder_config_section] = default_settings["task_recorder_settings"]
        self.__configparser[self.__alarm_config_section] = default_settings["alarm_settings"]
        self.__configparser[self.__music_player_config_section] = default_settings["music_player_settings"]

    def get_saved_preset_number_settings(self) -> PresetSettings:
        return {"preset_index": self.__configparser.getint(self.__timer_preset_config_section, "preset_index")}

    @staticmethod
    def get_preset_section(preset_index: int) -> str:
        return f"PRESET_{preset_index + 1}"

    def get_saved_timer_settings(self, preset_index: int) -> TimerSettings:
        section = self.get_preset_section(preset_index)
        return {
            "preset_name": self.__configparser.get(section, "preset_name"),
            "task_minutes": self.__configparser.getint(section, "task_minutes"),
            "short_break_minutes": self.__configparser.getint(section, "short_break_minutes"),
            "long_break_minutes": self.__configparser.getint(section, "long_break_minutes"),
            "loop_times": self.__configparser.getint(section, "loop_times"),
            "will_count": self.__configparser.getboolean(section, "will_count"),
            "count_seconds": self.__configparser.getint(section, "count_seconds")
        }

    def get_saved_task_recorder_settings(self) -> TaskRecorderSettings:
        return {
            "will_record_task": self.__configparser.getboolean(self.__task_recorder_config_section, "will_record_task"),
            "will_record_break": self.__configparser.getboolean(self.__task_recorder_config_section,
                                                                "will_record_break"),
            "file_format_index": self.__configparser.getint(self.__task_recorder_config_section, "file_format_index"),
            "save_file_path": self.__configparser.get(self.__task_recorder_config_section, "save_file_path"),
        }

    def get_saved_alarm_settings(self) -> AlarmSettings:
        return {"alarm_index": self.__configparser.getint(self.__alarm_config_section, "alarm_index")}

    def get_saved_music_player_settings(self) -> MusicPlayerSettings:
        return {
            "will_play_music": self.__configparser.getboolean(self.__music_player_config_section, "will_play_music"),
            "will_play_music_on_break": self.__configparser.getboolean(self.__music_player_config_section,
                                                                       "will_play_music_on_break"),
            "playlist_name": self.__configparser.get(self.__music_player_config_section, "playlist_name"),
            "is_random_mode": self.__configparser.getboolean(self.__music_player_config_section, "is_random_mode")}

    def get_saved_settings(self) -> AppSettings:
        return {"preset_index_settings": self.get_saved_preset_number_settings(),
                "timer_settings_list": [self.get_saved_timer_settings(i) for i in
                                        range(self.__default_settings.get_total_preset_number())],
                "task_recorder_settings": self.get_saved_task_recorder_settings(),
                "alarm_settings": self.get_saved_alarm_settings(),
                "music_player_settings": self.get_saved_music_player_settings()}

    def save(self) -> None:
        with open(self.__ini_file_path, "w", encoding=self.__encoder) as configfile:
            self.__configparser.write(configfile)

    def save_changed_settings(self, preset_index_settings, timer_settings_list, task_recorder_settings, alarm_settings,
                              music_player_settings) -> None:
        self.__configparser[self.__timer_preset_config_section] = preset_index_settings
        for i, settings in enumerate(timer_settings_list):
            self.__configparser[self.get_preset_section(i)] = settings
        self.__configparser[self.__task_recorder_config_section] = task_recorder_settings
        self.__configparser[self.__alarm_config_section] = alarm_settings
        self.__configparser[self.__music_player_config_section] = music_player_settings
        self.save()
