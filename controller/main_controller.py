from enum import Enum, auto
from typing import Callable, Final
import ui

from controller.appearance_controller import AppearanceController
from controller.alert_controller import AlertController
from controller.config_controller import ConfigurationController
from controller.task_edit_controller import TaskEditController
from controller.timer_controller import TimerController
from controller.ux_controller import UXController
from models.configuration.config_class.app_config import AppConfig


class CommandCategory(Enum):
    timer = auto()
    config = auto()
    task = auto()
    alert = auto()
    dialog = auto()
    preset = auto()


class KeyCommands:
    def __init__(self) -> None:
        self.__key_commands_list: Final[list[dict[str, str]]] = [
            # timer
            {'input': 'P', 'modifiers': 'cmd', 'title': 'play'},
            {'input': '\b', 'modifiers': 'cmd', 'title': 'clear'},
            # config
            {'input': 'M', 'modifiers': 'cmd', 'title': 'music'},
            {'input': 'I', 'modifiers': 'cmd', 'title': 'config'},
            # task
            {'input': 'T', 'modifiers': 'cmd', 'title': 'task'},
            # alert
            {'input': 'C', 'modifiers': 'cmd', 'title': 'interrupt'},
            {'input': '\r', 'modifiers': 'cmd', 'title': 'confirm'},
            # dialog
            {'input': 'D', 'modifiers': 'cmd', 'title': 'default'},
            {'input': 'S', 'modifiers': 'cmd', 'title': 'save'},
            # change preset
            {'input': '1', 'modifiers': 'cmd', 'title': 'preset'},
            {'input': '2', 'modifiers': 'cmd', 'title': 'preset'},
            {'input': '3', 'modifiers': 'cmd', 'title': 'preset'},
            {'input': '4', 'modifiers': 'cmd', 'title': 'preset'},
            {'input': '5', 'modifiers': 'cmd', 'title': 'preset'},
        ]

    def get_key_commands_list(self) -> list[dict[str, str]]:
        return self.__key_commands_list

    @staticmethod
    def categorize_command(sender) -> CommandCategory:
        if sender['title'] in ('play', 'clear'):
            return CommandCategory.timer
        if sender['title'] in ('music', 'config'):
            return CommandCategory.config
        if sender['title'] == 'task':
            return CommandCategory.task
        if sender['title'] in ('default', 'save'):
            return CommandCategory.dialog
        if sender['title'] == 'preset':
            return CommandCategory.preset
        return CommandCategory.alert


class MainController(ui.View):
    def __init__(self):
        self.name = "ポモドーロタイマー"
        self.__key_command = KeyCommands()

        # 画面レイアウト設定
        frame_width, frame_height = ui.get_screen_size()
        self.frame = (0, 0, frame_width, frame_height)
        self.__alert_controller: Final[AlertController] = \
            AlertController(frame_width, frame_height, self.add_subview, self.remove_subview)
        self.__appearance_controller: Final[AppearanceController] = AppearanceController(frame_width, frame_height)
        self.add_subview(self.__appearance_controller.get_appearance_instance())
        self.__appearance_controller.reset_background()

        # 設定
        self.__config_controller: ConfigurationController = ConfigurationController(
            alert_controller=self.__alert_controller, get_open_dialog_method=self.get_open_dialog_method,
            get_close_dialog_method=self.get_close_dialog_method, apply_renewal_config=self.apply_renewal_config
        )
        config = self.__config_controller.get_saved_config()

        # 設定の反映
        self.__ux_controller = UXController(config, self.__appearance_controller)
        self.__task_edit_controller: TaskEditController = TaskEditController(
            alert_controller=self.__alert_controller, get_open_dialog_method=self.get_open_dialog_method,
            get_close_dialog_method=self.get_close_dialog_method,
            set_recording_task_name=self.__ux_controller.set_recording_task_name
        )

        timer_config, alarm_config = None, None
        if config is not None:
            timer_config = config.get_specified_timer_config_preset()
            alarm_config = config.get_alarm_config()
        self.__timer_controller = TimerController(timer_config=timer_config,
                                                  alarm_config=alarm_config,
                                                  show_validation_error_message=self.show_validation_error_message,
                                                  set_ux_for_focus_mode=self.__ux_controller.set_ux_for_focus_mode,
                                                  set_ux_for_break_mode=self.__ux_controller.set_ux_for_break_mode,
                                                  reset_ux=self.__ux_controller.reset_ux,
                                                  start_task=self.__ux_controller.start_task,
                                                  interrupt_task=self.__ux_controller.interrupt_task
                                                  )

    def launch_app(self) -> None:
        self.__appearance_controller.display_appearance(
            displaying_task_view_instance=self.__task_edit_controller.get_displaying_task_view_instance(),
            timer_view_instance=self.__timer_controller.get_timer_view_instance(),
            config_button_view_instance=self.__config_controller.get_config_button_view_instance()
        )
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
            self.__timer_controller.execute_command(sender)
        if command_category == CommandCategory.preset:
            self.apply_timer_preset_config(int(sender['input']) - 1)

    def will_close(self) -> None:
        self.__timer_controller.reset()
        del self.__config_controller
        del self.__task_edit_controller
        del self.__ux_controller
        del self.__timer_controller
        del self.__alert_controller
        del self.__appearance_controller
        self.__config_controller = None
        self.__task_edit_controller = None

    def get_open_dialog_method(self, view_instance) -> Callable[[], None]:
        def open_dialog() -> None:
            self.__appearance_controller.disable_view()
            self.__timer_controller.stop_timer()
            self.add_subview(view_instance)
        return open_dialog

    def get_close_dialog_method(self, view_instance) -> Callable[[], None]:
        def close_dialog() -> None:
            self.__appearance_controller.enable_view()
            self.remove_subview(view_instance)
        return close_dialog

    def show_validation_error_message(self):
        alert_message = self.__config_controller.get_validation_error_message()
        self.__alert_controller.show_message_alert(alert_message)
    
    def apply_timer_preset_config(self, preset_index, will_apply_only_preset=True) -> None:
        self.__config_controller.change_timer_preset(preset_index)
        timer_config, alarm_config, preset_name = self.__config_controller.get_timer_config()
        self.__timer_controller.apply_renewal_config(timer_config, alarm_config)
        if will_apply_only_preset:
            self.__alert_controller.show_message_alert(f"プリセット『{preset_name}』に変更しました!")

    def apply_renewal_config(self, config: AppConfig, alert_message: str) -> None:
        self.apply_timer_preset_config(config.get_preset_index(), False)
        self.__ux_controller.apply_renewal_config(config.get_task_recorder_config(), config.get_music_player_config())
        self.__alert_controller.show_message_alert(alert_message)
