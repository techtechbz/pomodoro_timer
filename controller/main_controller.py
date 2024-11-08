from typing import Callable, Final
import ui

from controller.alert_controller import AlertController
from controller.appearance_controller import AppearanceController
from controller.config_controller import ConfigurationController
from controller.task_edit_controller import TaskEditController
from controller.ux_controller import UXController
from controller.key_command import CommandCategory, KeyCommand
from models.configuration.config_class.app_config import AppConfig


class MainController(ui.View):
    def __init__(self):
        self.name = "ポモドーロタイマー"
        self.__key_command: Final[KeyCommand] = KeyCommand()
        # 画面レイアウト設定
        frame_width, frame_height = ui.get_screen_size()
        self.frame = (0, 0, frame_width, frame_height)
        self.__appearance_controller: AppearanceController = AppearanceController(frame_width, frame_height)
        self.__alert_controller: AlertController = \
            AlertController(frame_width, frame_height, self.add_subview, self.remove_subview)

        self.__config_controller: ConfigurationController = ConfigurationController(
            alert_controller=self.__alert_controller, get_open_dialog_method=self.get_open_dialog_method,
            get_close_dialog_method=self.get_close_dialog_method, apply_renewal_config=self.apply_renewal_config
        )
        config = self.__config_controller.get_saved_config()
        self.__ux_controller = UXController(config, self.__appearance_controller, self.show_validation_error_message)
        self.__task_edit_controller: TaskEditController = TaskEditController(
            alert_controller=self.__alert_controller, get_open_dialog_method=self.get_open_dialog_method,
            get_close_dialog_method=self.get_close_dialog_method,
            set_recording_task_name=self.__ux_controller.set_recording_task_name
        )

    def launch_app(self) -> None:
        self.__appearance_controller.add_open_dialog_subview_instance(
            displaying_task_view_instance=self.__task_edit_controller.get_displaying_task_view_instance(),
            config_button_view_instance=self.__config_controller.get_config_button_view_instance()
        )
        self.add_subview(self.__appearance_controller.get_appearance_instance())
        self.__appearance_controller.reset_background()
        self.present("sheet")

    def layout(self) -> None:
        frame_width, frame_height = ui.get_screen_size()
        self.frame = (0, 0, frame_width, frame_height)
        self.__appearance_controller.sizing(frame_width, frame_height)
        self.__alert_controller.adjust_position(frame_width, frame_height)
        self.__config_controller.sizing(frame_width, frame_height)
        self.__task_edit_controller.sizing(frame_width, frame_height)
    
    def keyboard_frame_will_change(self, frame) -> None:
        padding_of_keyboard = self.height - frame[3]
        if self.__config_controller is not None:
            self.__config_controller.adjust_layout_for_keyboard_height(padding_of_keyboard)
        if self.__task_edit_controller is not None:
            self.__task_edit_controller.adjust_layout_for_keyboard_height(padding_of_keyboard)

    def get_key_commands(self) -> list[dict[str, str]]:
        return self.__key_command.get_key_commands_list()

    def key_command(self, sender: dict[str, str]) -> None:
        command_category = self.__key_command.categorize_command(sender)
        if command_category == CommandCategory.config or self.__config_controller.is_displaying_dialog():
            self.__config_controller.execute_command(sender)
            return
        if command_category == CommandCategory.task or self.__task_edit_controller.is_displaying_dialog():
            self.__task_edit_controller.execute_command(sender)
            return
        if command_category == CommandCategory.timer:
            self.__ux_controller.execute_command(sender)
        if command_category == CommandCategory.preset:
            self.apply_timer_preset_config(int(sender['input']) - 1)

    def will_close(self) -> None:
        self.__ux_controller.reset_ux()
        del self.__ux_controller
        del self.__appearance_controller
        del self.__alert_controller
        del self.__config_controller
        del self.__task_edit_controller

    def get_open_dialog_method(self, view_instance) -> Callable[[], None]:
        def open_dialog() -> None:
            self.__appearance_controller.disable_view()
            self.__ux_controller.stop_timer()
            self.add_subview(view_instance)
        return open_dialog

    def get_close_dialog_method(self, view_instance) -> Callable[[], None]:
        def close_dialog() -> None:
            self.__appearance_controller.enable_view()
            self.remove_subview(view_instance)
        return close_dialog

    def apply_timer_preset_config(self, preset_index: int) -> None:
        self.__config_controller.change_timer_preset(preset_index)
        preset_name = self.__config_controller.get_preset_name()
        self.__ux_controller.apply_timer_config(self.__config_controller.get_saved_config())
        self.__alert_controller.show_message_alert(f"プリセット『{preset_name}』に変更しました!")

    def apply_renewal_config(self, config: AppConfig, alert_message: str) -> None:
        self.__ux_controller.apply_renewal_config(config)
        self.__alert_controller.show_message_alert(alert_message)

    def show_validation_error_message(self):
        alert_message = self.__config_controller.get_validation_error_message()
        self.__alert_controller.show_message_alert(alert_message)
