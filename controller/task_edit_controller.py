import ui
from typing import Callable, Final

from controller.alert_controller import AlertController
from custom_types.command import Command
from views.dialog.task_edit_view import TaskEditDialogViewManager
from views.appearance.displaying_task_view import DisplayingTaskViewManager


class TaskEditController:
    def __init__(self, alert_controller: AlertController,
                 get_open_dialog_method: Callable[[ui.View], Callable[[], None]],
                 get_close_dialog_method: Callable[[ui.View], Callable[[], None]],
                 set_recording_task_name: Callable[[str], None]) -> None:
        self.__alert_controller: Final[AlertController] = alert_controller
        self.set_recording_task_name = set_recording_task_name
        self.__task_edit_dialog_manager: Final[TaskEditDialogViewManager] = TaskEditDialogViewManager()
        self.__task_edit_dialog_manager.set_button_action(self.show_checking_to_set_task_alert,
                                                          self.show_checking_to_cancel_alert)
        self.open_dialog: Final[Callable[[], None]] = \
            get_open_dialog_method(self.__task_edit_dialog_manager.get_view_instance())
        self.close_dialog: Final[Callable[[], None]] = \
            get_close_dialog_method(self.__task_edit_dialog_manager.get_view_instance())

        self.__displaying_task_view_manager: Final[DisplayingTaskViewManager] = DisplayingTaskViewManager()
        self.__displaying_task_view_manager.set_edit_task_action(self.open_task_edit_dialog)
        self.__is_displaying_dialog = False

    def sizing(self, frame_width: float, frame_height: float) -> None:
        self.__task_edit_dialog_manager.sizing(frame_width, frame_height)

    def adjust_layout_for_keyboard_height(self, padding_of_keyboard: float) -> None:
        self.__task_edit_dialog_manager.adjust_layout_for_keyboard_height(padding_of_keyboard)

    def get_displaying_task_view_instance(self) -> ui.View:
        return self.__displaying_task_view_manager.get_view_instance()

    def is_displaying_dialog(self) -> bool:
        return self.__is_displaying_dialog

    def open_task_edit_dialog(self, _=None) -> None:
        self.open_dialog()
        self.__is_displaying_dialog = True

    def close_task_edit_dialog(self) -> None:
        self.close_dialog()
        self.__is_displaying_dialog = False
        self.__task_edit_dialog_manager.enable_view()

    def execute_command(self, sender: Command) -> None:
        if sender['title'] == 'task':
            self.open_task_edit_dialog()
        if self.__alert_controller.is_displayed_alert():
            self.__alert_controller.execute_command(sender)
            return
        if sender['title'] == 'save':
            self.show_checking_to_set_task_alert()
        if sender['title'] == 'interrupt':
            self.show_checking_to_cancel_alert()

    def show_checking_to_set_task_alert(self, _=None) -> None:
        self.__task_edit_dialog_manager.disable_view()
        self.__alert_controller.show_choice_alert("タスクを設定しますか?", self.set_new_task, self.cancel)

    def show_checking_to_cancel_alert(self, _=None) -> None:
        self.__task_edit_dialog_manager.disable_view()
        self.__alert_controller.show_choice_alert("タスクを編集せずに終了しますか?", self.interrupt_edit, self.cancel)

    def set_new_task(self, _=None) -> None:
        self.__alert_controller.close_choice_alert()
        new_task_name = self.__task_edit_dialog_manager.get_input_task_name()
        self.set_recording_task_name(new_task_name)
        self.__displaying_task_view_manager.update_task_name_label(new_task_name)
        self.close_task_edit_dialog()
        self.__alert_controller.show_message_alert("タスクを設定しました!")

    def cancel(self, _=None) -> None:
        self.__alert_controller.close_choice_alert()
        self.__task_edit_dialog_manager.enable_view()

    def interrupt_edit(self, _=None) -> None:
        current_task_name = self.__displaying_task_view_manager.get_current_task_name()
        self.__task_edit_dialog_manager.set_previous_task_name(current_task_name)
        self.__alert_controller.close_choice_alert()
        self.close_task_edit_dialog()
