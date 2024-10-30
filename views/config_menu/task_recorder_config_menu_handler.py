import os
import ui

from models.task_recorder import FileFormat


class TaskRecorderConfigMenuHandler:
	def __init__(self, current_task_recorder_settings):
		self.__task_recorder_config_view_class = ui.load_view("./pyui/config_menu/task_recorder_config_menu.pyui")
		self.__current_task_recorder_settings = current_task_recorder_settings
		self.__task_recorder_config_view_class["suggest_save_file_path_button"].action = self.suggest_file_path

	def get_view_instance(self):
		return self.__task_recorder_config_view_class
	
	def reset_settings(self, task_recorder_settings):
		self.__current_task_recorder_settings = task_recorder_settings
		self.insert_field_text()
	
	def suggest_file_path(self, _):
		self.__task_recorder_config_view_class["save_file_path_input"].text = f'{os.getcwd()}/task_records'
	
	def write_out_field_inputs(self):
		self.__current_task_recorder_settings["will_record_task"] = \
			self.__task_recorder_config_view_class["will_record_task_switch"].value
		self.__current_task_recorder_settings["will_record_break"] = \
			self.__task_recorder_config_view_class["will_record_break_switch"].value
		self.__current_task_recorder_settings["file_format_index"] = \
			self.__task_recorder_config_view_class["file_format_segmented_control"].selected_index
		self.__current_task_recorder_settings["save_file_path"] = \
			self.__task_recorder_config_view_class["save_file_path_input"].text
	
	def insert_field_text(self):
		self.__task_recorder_config_view_class["will_record_task_switch"].value = \
			self.__current_task_recorder_settings["will_record_task"]
		
		self.__task_recorder_config_view_class["will_record_break_switch"].value = \
			self.__current_task_recorder_settings["will_record_break"]
		
		self.__task_recorder_config_view_class["file_format_segmented_control"].segments = FileFormat.get_file_format_list()
		self.__task_recorder_config_view_class["file_format_segmented_control"].selected_index = \
			self.__current_task_recorder_settings["file_format_index"]
		
		self.__task_recorder_config_view_class["save_file_path_input"].text = \
			self.__current_task_recorder_settings["save_file_path"]
	
	def get_setting_values(self):
		return self.__current_task_recorder_settings
