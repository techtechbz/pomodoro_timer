import ui


class TaskEditDialogViewManager:
	def __init__(self):
		self.__view_instance = ui.load_view("./pyui/dialog/task_edit_dialog.pyui")
	
	def get_view_instance(self):
		return self.__view_instance

	def adjust_to_center(self, frame_width, frame_height):
		self.__view_instance.center = (frame_width * 0.5, frame_height * 0.5)

	def get_scale_factor(self, frame_width):
		return frame_width / self.__view_instance.width * 0.8
	
	def sizing(self, frame_width, frame_height):
		self.adjust_to_center(frame_width, frame_height)
		scale_factor = self.get_scale_factor(frame_width)
		if self.__view_instance.width > frame_width:
			self.__view_instance.transform = ui.Transform.scale(scale_factor, scale_factor)
	
	def adjust_layout_for_keyboard_height(self, padding_of_keyboard):
		frame_width, frame_height = ui.get_screen_size()
		padding = frame_height / 30
		view_class_length = self.__view_instance.y + self.__view_instance.height
		if padding_of_keyboard < view_class_length:
			vertical_axis = self.__view_instance.y - view_class_length + padding_of_keyboard - padding
			if vertical_axis < self.__view_instance.y:
				vertical_axis /= 2.5
			self.__view_instance.y = vertical_axis
		else:
			self.adjust_to_center(frame_width, frame_height)
	
	def set_previous_task_name(self, task_name):
		self.__view_instance["task_name_field"].text = task_name
	
	def get_input_task_name(self):
		return self.__view_instance["task_name_field"].text

	def set_button_action(self, save_edition_action, cancel_edition_action):
		self.__view_instance['save_edition_button'].action = save_edition_action
		self.__view_instance['cancel_edition_button'].action = cancel_edition_action

	def switch_view_enabled(self, will_enabled):
		for subview in self.__view_instance.subviews:
			if hasattr(subview, 'enabled'):
				subview.enabled = will_enabled
	
	def enable_view(self):
		self.__view_instance.touch_enabled = True
		self.switch_view_enabled(True)
		self.__view_instance.alpha = 1.0
	
	def disable_view(self):
		self.__view_instance.touch_enabled = False
		self.switch_view_enabled(False)
		self.__view_instance.alpha = 0.2
