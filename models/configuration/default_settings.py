from typing import Final

from custom_types.settings import PresetSettings, TimerSettings, TimerSettingsList, AlarmSettings, \
	MusicPlayerSettings, TaskRecorderSettings, AppSettings


class DefaultSettings:
	def __init__(self) -> None:
		self.__total_preset_number: Final[int] = 5
		self.__default_timer_preset_settings: Final[PresetSettings] = {"preset_index": 0}
		self.__default_timer_settings: Final[TimerSettings] = {
			"preset_name": "",
			"task_minutes": 25,
			"short_break_minutes": 5,
			"long_break_minutes": 60,
			"loop_times": 4,
			"will_count": True,
			"count_seconds": 5
		}
		self.__default_task_recorder_settings: Final[TaskRecorderSettings] = {
			"will_record_task": False,
			"will_record_break": False,
			"file_format_index": 0,
			"save_file_path": ""
		}
		self.__default_alarm_settings: Final[AlarmSettings] = {
			"alarm_index": 0,
			"will_notice": False,
			"notice_seconds": 0
		}
		self.__default_music_player_settings: Final[MusicPlayerSettings] = {
			"will_play_music": False,
			"will_play_music_on_break": False,
			"playlist_name": "",
			"is_random_mode": False
		}
		
	def get_total_preset_number(self) -> int:
		return self.__total_preset_number
	
	def get_default_timer_settings(self, preset_index: int) -> TimerSettings:
		settings = self.__default_timer_settings.copy()
		settings["preset_name"] = f'プリセット{preset_index+1}'
		return settings
	
	def get_default_timer_settings_list(self) -> TimerSettingsList:
		return [self.get_default_timer_settings(i) for i in range(self.__total_preset_number)]

	def get_default_settings(self) -> AppSettings:
		return {
			"preset_index_settings": self.__default_timer_preset_settings.copy(),
			"timer_settings_list": self.get_default_timer_settings_list(),
			"task_recorder_settings": self.__default_task_recorder_settings.copy(),
			"alarm_settings": self.__default_alarm_settings.copy(),
			"music_player_settings": self.__default_music_player_settings.copy()
		}
