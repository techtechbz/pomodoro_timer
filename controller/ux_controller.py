import console
from objc_util import on_main_thread

from models.configuration.config_class.task_recorder_config import TaskRecorderConfig
from models.configuration.config_class.music_player_config import MusicPlayerConfig
from models.task_recorder.task_recorder import TaskRecorder
from models.sound.music_player import MusicPlayer


class UXController:
    def __init__(self, task_recorder_config: TaskRecorderConfig, music_player_config: MusicPlayerConfig) -> None:
        self.__task_recorder = TaskRecorder(task_recorder_config)
        self.__music_player = MusicPlayer(music_player_config)

    def apply_renewal_config(self, task_recorder_config: TaskRecorderConfig,
                             music_player_config: MusicPlayerConfig) -> None:
        self.__task_recorder.apply_task_recorder_config(task_recorder_config)
        self.__music_player.apply_renewal_config(music_player_config)
    
    @staticmethod
    def display_screen_eternally(flag) -> None:
        on_main_thread(console.set_idle_timer_disabled)(flag)

    def set_ux_for_focus_mode(self) -> None:
        self.__task_recorder.start_task()
        self.__music_player.change_mode(False)

    def set_ux_for_break_mode(self) -> None:
        self.__task_recorder.interrupt_task()
        self.__music_player.change_mode(True)

    def reset_ux(self) -> None:
        self.__task_recorder.save_task_record()
        self.__music_player.stop_music()

    def start_task(self, on_break: bool) -> None:
        self.__task_recorder.start_task()
        self.__music_player.restart_music(on_break)

    def interrupt_task(self) -> None:
        self.__task_recorder.interrupt_task()
        self.__music_player.pause_music()

    def set_recording_task_name(self, task_name: str) -> None:
        self.__task_recorder.set_task_name(task_name)

