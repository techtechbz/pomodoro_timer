class DefaultSettings:
	def __init__(self):
		self.__total_preset_number = 5
		self.__default_timer_preset_settings = {"preset_index": 0}
		self.__default_timer_settings = {
			"preset_name": "",
			"task_minutes": 25,
			"short_break_minutes": 5,
			"long_break_minutes": 60,
			"loop_times": 4,
			"will_count": True,
			"count_seconds": 5
		}
		self.__default_task_recorder_settings = {
			"will_record_task": False,
			"will_record_break": False,
			"file_format_index": 0,
			"save_file_path": "",
		}
		self.__default_alarm_settings = {"alarm_index": 0}
		self.__default_music_player_settings = {
			"will_play_music": False,
			"will_play_music_on_break": False,
			"playlist_name": "",
			"is_random_mode": False
		}
		
	def get_total_preset_number(self):
		return self.__total_preset_number
	
	def get_default_timer_settings(self, preset_index):
		settings = self.__default_timer_settings.copy()
		settings["preset_name"] = f'プリセット{preset_index+1}'
		return settings
	
	def get_default_timer_settings_list(self):
		return [self.get_default_timer_settings(i) for i in range(self.__total_preset_number)]

	def get_default_settings(self):
		return {
			"preset_index_settings": self.__default_timer_preset_settings.copy(),
			"timer_settings_list": self.get_default_timer_settings_list(),
			"task_recorder_settings": self.__default_task_recorder_settings.copy(),
			"alarm_settings": self.__default_alarm_settings.copy(),
			"music_player_settings": self.__default_music_player_settings.copy()
		}
