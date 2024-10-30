from views.appearance.appearance_view import AppearanceViewManager


class AppearanceController:
    def __init__(self, frame_width: int, frame_height: int) -> None:
        self.__appearance_manager = AppearanceViewManager(frame_width, frame_height)

    def sizing(self, frame_width: int, frame_height: int) -> None:
        self.__appearance_manager.sizing(frame_width, frame_height)

    def get_appearance_instance(self):
        return self.__appearance_manager.get_view_instance()

    def display_appearance(self, displaying_task_view_instance, timer_view_instance,
                           config_button_view_instance) -> None:
        self.__appearance_manager.display_subview(displaying_task_view_instance, timer_view_instance,
                                                  config_button_view_instance)

    def change_background_for_focus_mode(self) -> None:
        self.__appearance_manager.change_to_focus_mode()

    def change_background_for_break_mode(self) -> None:
        self.__appearance_manager.change_to_break_mode()

    def reset_background(self) -> None:
        self.__appearance_manager.reset()

    def enable_view(self):
        self.get_appearance_instance().touch_enabled = True
        self.__appearance_manager.switch_view_enabled(True)
        self.get_appearance_instance().alpha = 1.0

    def disable_view(self):
        self.get_appearance_instance().touch_enabled = False
        self.__appearance_manager.switch_view_enabled(False)
        self.get_appearance_instance().alpha = 0.2
