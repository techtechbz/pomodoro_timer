import ui


class AppearanceViewManager:
	def __init__(self, frame_width: int, frame_height: int) -> None:
		self.__view_instance = ui.load_view("./pyui/appearance/appearance.pyui")
		self.__default_background_color = "#ffffff"
		self.__focus_mode_background_color = "#ff9f9f"
		self.__break_mode_background_color = "#b7cfff"
		self.sizing(frame_width, frame_height)

	def get_view_instance(self):
		return self.__view_instance

	def sizing(self, frame_width: int, frame_height: int) -> None:
		self.__view_instance.center = (frame_width * 0.5, frame_height * 0.45)
		if frame_width > frame_height:
			scale_factor = frame_height / self.__view_instance.height
			self.__view_instance.y = (self.__view_instance.height - frame_height) * 0.05
		else:
			scale_factor = frame_width / self.__view_instance.width
		self.__view_instance.transform = ui.Transform.scale(scale_factor, scale_factor)

	def display_subview(self, displaying_task_view_instance, timer_view_instance, config_button_view_instance) -> None:
		self.__view_instance['displaying_task_view'].add_subview(displaying_task_view_instance)
		self.__view_instance['timer_view'].add_subview(timer_view_instance)
		self.__view_instance['config_button_view'].add_subview(config_button_view_instance)

	def change_to_focus_mode(self) -> None:
		self.__view_instance.superview.background_color = self.__focus_mode_background_color
		self.__view_instance.background_color = self.__focus_mode_background_color

	def change_to_break_mode(self) -> None:
		self.__view_instance.superview.background_color = self.__break_mode_background_color
		self.__view_instance.background_color = self.__break_mode_background_color

	def reset(self) -> None:
		self.__view_instance.superview.background_color = self.__default_background_color
		self.__view_instance.background_color = self.__default_background_color

	def switch_view_enabled(self, will_enabled) -> None:
		for subview in self.__view_instance.subviews:
			for sub in subview.subviews:
				for s in sub.subviews:
					if hasattr(s, 'enabled'):
						s.enabled = will_enabled
					if hasattr(s, 'touch_enabled'):
						s.touch_enabled = will_enabled
