from sound import play_effect
from typing import Optional

from controller.appearance_controller import AppearanceController
from controller.ux_controller import UXController
from custom_types.command import Command
from models.pomodoro_timer import PomodoroTimer
from models.configuration.config_class.alarm_config import AlarmConfig
from models.configuration.config_class.app_config import AppConfig
from models.configuration.config_class.music_player_config import MusicPlayerConfig
from models.configuration.config_class.task_recorder_config import TaskRecorderConfig
from models.configuration.config_class.timer_config import TimerConfig
from views.appearance.timer_view import TimerViewManager


class TimerController:
    def __init__(self, config: Optional[AppConfig], appearance_controller: AppearanceController,
                 show_validation_error_message):
        self.__timer_view_manager = TimerViewManager()
        self.__appearance_controller = appearance_controller
        self.__appearance_controller.add_timer_subview_instance(self.__timer_view_manager.get_view_instance())
        self.__timer, self.__ux_controller = None, None
        if config is None:
            self.__timer_view_manager.set_button_action(show_validation_error_message, self.clear_timer)
            return
        self.apply_renewal_config(config)

    def define_timer_instance(self, timer_config: TimerConfig, alarm_config: AlarmConfig) -> None:
        self.__timer = PomodoroTimer(timer_config=timer_config,
                                     alarm_config=alarm_config,
                                     timer_view_manager=self.__timer_view_manager,
                                     change_ux_to_focus_mode=self.change_ux_to_focus_mode,
                                     change_ux_to_break_mode=self.change_ux_to_break_mode)

    def define_ux_controller(self, task_recorder_config: TaskRecorderConfig, music_player_config: MusicPlayerConfig)\
            -> None:
        self.__ux_controller = UXController(task_recorder_config, music_player_config)

    def apply_renewal_timer_config(self, timer_config: TimerConfig, alarm_config: AlarmConfig) -> None:
        self.reset()
        self.__timer.apply_renewal_config(timer_config, alarm_config)

    def apply_renewal_config(self, config: Optional[AppConfig]) -> None:
        if config is None:
            return
        self.reset()

        timer_config = config.get_specified_timer_config_preset()
        alarm_config = config.get_alarm_config()
        task_recorder_config = config.get_task_recorder_config()
        music_player_config = config.get_music_player_config()

        if self.__timer is None:
            self.define_ux_controller(task_recorder_config, music_player_config)
            self.define_timer_instance(timer_config, alarm_config)
            self.__timer_view_manager.set_button_action(self.play_timer, self.clear_timer)
            return
        self.__ux_controller.apply_renewal_config(task_recorder_config, music_player_config)
        self.__timer.apply_renewal_config(timer_config, alarm_config)

    def set_recording_task_name(self, task_name: str) -> None:
        self.__ux_controller.set_recording_task_name(task_name)

    def execute_command(self, sender: Command) -> None:
        if sender['title'] == 'play':
            self.play_timer()
        if sender['title'] == 'clear':
            self.clear_timer()

    @staticmethod
    def effect_pushing_button_sound() -> None:
        play_effect('ui:switch33')

    def start_timer(self) -> None:
        self.__timer_view_manager.change_play_timer_button_title("STOP")
        self.__timer.start_timer()
        self.__ux_controller.start_task(self.__timer.on_break())

    def stop_timer(self) -> None:
        if self.__timer is None:
            return
        self.__timer.stop_timer()
        self.__timer_view_manager.change_play_timer_button_title("START")
        self.__ux_controller.interrupt_task()

    def play_timer(self, _=None) -> None:
        self.effect_pushing_button_sound()
        if self.__timer.is_running():
            self.stop_timer()
        else:
            self.start_timer()

    def reset(self) -> None:
        if self.__timer is not None:
            self.__timer.clear()
            self.stop_timer()
            self.__appearance_controller.reset_background()
            self.__ux_controller.reset_ux()

    def clear_timer(self, _=None) -> None:
        self.effect_pushing_button_sound()
        self.reset()

    def change_ux_to_focus_mode(self) -> None:
        self.__appearance_controller.change_background_for_focus_mode()
        self.__ux_controller.set_ux_for_focus_mode()

    def change_ux_to_break_mode(self) -> None:
        self.__appearance_controller.change_background_for_break_mode()
        self.__ux_controller.set_ux_for_break_mode()
