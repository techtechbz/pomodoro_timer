import console
from objc_util import on_main_thread
from typing import Optional

from controller.appearance_controller import AppearanceController
from controller.timer_controller import TimerController
from models.configuration.config_class.app_config import AppConfig
from models.task_recorder.task_recorder import TaskRecorder
from models.sound.music_player import MusicPlayer


class UXController:
    def __init__(self, config: Optional[AppConfig], appearance_controller: AppearanceController,
                 show_validation_error_message):
        self.__appearance_controller = appearance_controller
        self.__task_recorder: Optional[TaskRecorder] = None
        self.__music_player: Optional[MusicPlayer] = None
        # 設定
        timer_config, alarm_config = None, None
        if config is not None:
            timer_config = config.get_specified_timer_config_preset()
            alarm_config = config.get_alarm_config()
            self.define_functions_instance(config.get_task_recorder_config(), config.get_music_player_config())
        self.__timer_controller = TimerController(timer_config=timer_config,
                                                  alarm_config=alarm_config,
                                                  show_validation_error_message=show_validation_error_message,
                                                  set_ux_for_focus_mode=self.set_ux_for_focus_mode,
                                                  set_ux_for_break_mode=self.set_ux_for_break_mode,
                                                  reset_ux=self.reset_ux,
                                                  start_task=self.start_task,
                                                  interrupt_task=self.interrupt_task
                                                  )
        self.__appearance_controller.add_timer_subview_instance(self.__timer_controller.get_timer_view_instance())

    def execute_command(self, sender) -> None:
        self.__timer_controller.execute_command(sender)

    def define_functions_instance(self, task_recorder_config, music_player_config) -> None:
        self.__task_recorder = TaskRecorder(task_recorder_config)
        self.__music_player = MusicPlayer(music_player_config)

    @staticmethod
    def display_screen_eternally(flag) -> None:
        on_main_thread(console.set_idle_timer_disabled)(flag)

    def set_ux_for_focus_mode(self) -> None:
        self.__task_recorder.start_task()
        self.__appearance_controller.change_background_for_focus_mode()
        self.__music_player.change_to_focus_mode()

    def set_ux_for_break_mode(self) -> None:
        self.__task_recorder.interrupt_task()
        self.__appearance_controller.change_background_for_break_mode()
        self.__music_player.change_to_break_mode()

    def reset_ux(self) -> None:
        self.__task_recorder.save_task_record()
        self.__appearance_controller.reset_background()
        self.__music_player.stop_music()

    def start_task(self, on_break: bool) -> None:
        self.__task_recorder.start_task()
        self.__music_player.restart_music(on_break)
        self.display_screen_eternally(True)

    def interrupt_task(self) -> None:
        self.__task_recorder.interrupt_task()
        self.__music_player.pause_music()
        self.display_screen_eternally(False)

    def stop_timer(self) -> None:
        self.__timer_controller.stop_timer()

    def apply_timer_config(self, config: AppConfig) -> None:
        self.__timer_controller.apply_renewal_config(
            config.get_specified_timer_config_preset(), config.get_alarm_config()
        )

    def apply_renewal_config(self, config: AppConfig) -> None:
        self.apply_timer_config(config)
        if self.__task_recorder is None:
            self.define_functions_instance(config.get_task_recorder_config(), config.get_music_player_config())
        else:
            self.__task_recorder.apply_task_recorder_config(config.get_task_recorder_config())
            self.__music_player.apply_renewal_config(config.get_music_player_config())

    def set_recording_task_name(self, task_name: str) -> None:
        self.__task_recorder.set_task_name(task_name)
