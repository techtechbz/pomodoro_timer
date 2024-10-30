import ui


class TimerConfigMenuHandler:
	def __init__(self, current_preset_index, current_timer_settings_list):
		self.__timer_config_view_class = ui.load_view("./pyui/config_menu/timer_config_menu.pyui")
		self.__current_preset_index = current_preset_index
		self.__current_timer_settings_list = current_timer_settings_list
		self.__timer_config_view_class["timer_preset_segmented_control"].segments = \
			[str(i + 1) for i in range(len(current_timer_settings_list))]
		self.__timer_config_view_class["timer_preset_segmented_control"].action = self.switch_preset
		self.set_textfield_keyboard()
	
	def set_textfield_keyboard(self):
		self.__timer_config_view_class["task_minutes_input"].keyboard_type = ui.KEYBOARD_NUMBERS
		self.__timer_config_view_class["short_break_minutes_input"].keyboard_type = ui.KEYBOARD_NUMBERS
		self.__timer_config_view_class["long_break_minutes_input"].keyboard_type = ui.KEYBOARD_NUMBERS
		self.__timer_config_view_class["loop_times_input"].keyboard_type = ui.KEYBOARD_NUMBERS
		self.__timer_config_view_class["count_seconds_input"].keyboard_type = ui.KEYBOARD_NUMBERS
	
	def get_view_instance(self):
		return self.__timer_config_view_class
		
	def reset_settings(self, preset_index: int, timer_settings_list):
		self.__current_preset_index = preset_index
		self.__current_timer_settings_list = timer_settings_list
		self.insert_field_text()

	def write_out_field_inputs(self):
		previous_preset_index = self.__current_preset_index
		self.__current_preset_index = self.__timer_config_view_class["timer_preset_segmented_control"].selected_index
		self.__current_timer_settings_list[previous_preset_index] = {
			"preset_name": self.__timer_config_view_class["preset_name_input"].text,
			"task_minutes": self.__timer_config_view_class["task_minutes_input"].text,
			"short_break_minutes": self.__timer_config_view_class["short_break_minutes_input"].text, 
			"long_break_minutes": self.__timer_config_view_class["long_break_minutes_input"].text,
			"loop_times": self.__timer_config_view_class["loop_times_input"].text,
			"will_count": self.__timer_config_view_class["will_count_switch"].value,
			"count_seconds": self.__timer_config_view_class["count_seconds_input"].text
		}
	
	def insert_field_text(self, preset_index=None):
		if preset_index is None:
			preset_index = self.__current_preset_index
			self.__timer_config_view_class["timer_preset_segmented_control"].selected_index = preset_index
		settings = self.__current_timer_settings_list[preset_index]
		self.__timer_config_view_class["preset_name_input"].text = str(settings["preset_name"])
		self.__timer_config_view_class["task_minutes_input"].text = str(settings["task_minutes"])
		self.__timer_config_view_class["short_break_minutes_input"].text = str(settings["short_break_minutes"])
		self.__timer_config_view_class["long_break_minutes_input"].text = str(settings["long_break_minutes"])
		self.__timer_config_view_class["loop_times_input"].text = str(settings["loop_times"])
		self.__timer_config_view_class["will_count_switch"].value = settings["will_count"]
		self.__timer_config_view_class["count_seconds_input"].text = str(settings["count_seconds"])
	
	def switch_preset(self, sender):
		switched_preset_index = sender.superview["timer_preset_segmented_control"].selected_index
		self.write_out_field_inputs()
		self.insert_field_text(switched_preset_index)
	
	def get_setting_values(self):
		return self.__current_preset_index, self.__current_timer_settings_list
