import ui

from models.sound.sound_effect import AlarmName


class AlarmConfigMenuHandler:
	def __init__(self, current_alarm_settings) -> None:
		self.__alarm_config_view_class = ui.load_view("./pyui/config_menu/alarm_config_menu.pyui")
		self.__current_alarm_settings = current_alarm_settings
		self.__alarm_config_view_class["notice_seconds_input"].keyboard_type = ui.KEYBOARD_NUMBERS

	def get_view_instance(self) -> ui.View:
		return self.__alarm_config_view_class

	def reset_settings(self, alarm_settings) -> None:
		self.__current_alarm_settings = alarm_settings
		self.insert_field_text()
	
	def write_out_field_inputs(self) -> None:
		self.__current_alarm_settings["alarm_index"] = \
			self.__alarm_config_view_class["alarm_name_segmented_control"].selected_index
		self.__current_alarm_settings["will_notice"] = self.__alarm_config_view_class["will_notice_switch"].value
		self.__current_alarm_settings["notice_seconds"] = self.__alarm_config_view_class["notice_seconds_input"].text
	
	def insert_field_text(self) -> None:
		self.__alarm_config_view_class["alarm_name_segmented_control"].segments = AlarmName.get_alarm_list()
		self.__alarm_config_view_class["alarm_name_segmented_control"].selected_index = \
			self.__current_alarm_settings["alarm_index"]
		self.__alarm_config_view_class["will_notice_switch"].value = self.__current_alarm_settings["will_notice"]
		self.__alarm_config_view_class["notice_seconds_input"].text = str(self.__current_alarm_settings["notice_seconds"])
	
	def get_setting_values(self):
		return self.__current_alarm_settings
