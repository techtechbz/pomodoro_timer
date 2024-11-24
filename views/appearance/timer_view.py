import ui


class TimerViewManager:
	def __init__(self):
		self.__view_instance = ui.load_view("./pyui/appearance/timer.pyui")

	def get_view_instance(self) -> ui.View:
		return self.__view_instance
	
	def set_button_action(self, play_timer_action, clear_timer_action) -> None:
		self.__view_instance["play_timer_button"].action = play_timer_action
		self.__view_instance["clear_timer_button"].action = clear_timer_action

	def update_remain_loop_label(self, remain_loop: int) -> None:
		self.__view_instance["remain_loop_label"].text = f"長時間休憩まで残り{remain_loop}回"
	
	def update_displayed_minutes(self, minutes: int) -> None:
		self.__view_instance['minutes'].text = str(minutes).zfill(2)
	
	def update_displayed_seconds(self, seconds: int) -> None:
		self.__view_instance['seconds'].text = str(seconds).zfill(2)
	
	def change_play_timer_button_title(self, title: str) -> None:
		self.__view_instance['play_timer_button'].title = title
