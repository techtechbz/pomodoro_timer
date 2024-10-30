import console
from objc_util import on_main_thread
from typing import Final, Optional

from controller.appearance_controller import AppearanceController
from models.configuration.config_class.app_config import AppConfig
from models.task_recorder import TaskRecorder
from models.sound.music_player import MusicPlayer


class UXController:
    def __init__(self, config: Optional[AppConfig], appearance_controller: AppearanceController):
        self.__appearance_controller: Final[AppearanceController] = appearance_controller
        self.__task_recorder: Optional[TaskRecorder] = None
        self.__music_player: Optional[MusicPlayer] = None
        if config is not None:
            self.define_functions_instance(config.get_task_recorder_config(), config.get_music_player_config())

    def define_functions_instance(self, task_recorder_config, music_player_config) -> None:
        self.__task_recorder: TaskRecorder = TaskRecorder(task_recorder_config)
        self.__music_player: MusicPlayer = MusicPlayer(music_player_config)

    def apply_renewal_config(self, task_recorder_config, music_player_config) -> None:
        if self.__task_recorder is None:
            self.define_functions_instance(task_recorder_config, music_player_config)
            return
        self.__task_recorder.apply_task_recorder_config(task_recorder_config)
        self.__music_player.apply_renewal_config(music_player_config)

    def set_recording_task_name(self, task_name: str) -> None:
        self.__task_recorder.set_task_name(task_name)

    @staticmethod
    def display_screen_eternally(flag) -> None:
        on_main_thread(console.set_idle_timer_disabled)(flag)

    def set_ux_for_focus_mode(self) -> None:
        self.__appearance_controller.change_background_for_focus_mode()
        self.__task_recorder.start_task()
        self.__music_player.change_to_focus_mode()

    def set_ux_for_break_mode(self) -> None:
        self.__appearance_controller.change_background_for_break_mode()
        self.__task_recorder.interrupt_task()
        self.__music_player.change_to_break_mode()

    def reset_ux(self) -> None:
        self.__appearance_controller.reset_background()
        self.__music_player.stop_music()
        self.__task_recorder.save_task_record()

    def start_task(self, on_break: bool) -> None:
        self.__task_recorder.start_task()
        self.__music_player.restart_music(on_break)
        self.display_screen_eternally(True)

    def interrupt_task(self):
        self.__task_recorder.interrupt_task()
        self.__music_player.pause_music()
        self.display_screen_eternally(False)
