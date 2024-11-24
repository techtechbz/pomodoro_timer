import ui

from views.appearance.appearance_view import AppearanceViewManager


class AppearanceController:
    def __init__(self, frame_width: int, frame_height: int) -> None:
        self.__appearance_manager = AppearanceViewManager(frame_width, frame_height)

    def sizing(self, frame_width: int, frame_height: int) -> None:
        self.__appearance_manager.sizing(frame_width, frame_height)

    def get_appearance_instance(self) -> ui.View:
        return self.__appearance_manager.get_view_instance()

    def add_timer_subview_instance(self, timer_view_instance: ui.View) -> None:
        self.__appearance_manager.add_timer_subview_instance(timer_view_instance)

    def add_open_dialog_subview_instance(self, displaying_task_view_instance, config_button_view_instance) -> None:
        self.__appearance_manager.add_open_dialog_subview_instance(
            displaying_task_view_instance, config_button_view_instance
        )

    def change_background_for_focus_mode(self) -> None:
        self.__appearance_manager.change_to_focus_mode()

    def change_background_for_break_mode(self) -> None:
        self.__appearance_manager.change_to_break_mode()

    def reset_background(self) -> None:
        self.__appearance_manager.reset()

    def enable_view(self) -> None:
        self.get_appearance_instance().touch_enabled = True
        self.__appearance_manager.switch_view_enabled(True)
        self.get_appearance_instance().alpha = 1.0

    def disable_view(self) -> None:
        self.get_appearance_instance().touch_enabled = False
        self.__appearance_manager.switch_view_enabled(False)
        self.get_appearance_instance().alpha = 0.2
