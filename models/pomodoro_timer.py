import threading
import time
from threading import Thread
from typing import Optional

from models.configuration.config_class.alarm_config import AlarmConfig
from models.configuration.config_class.timer_config import TimerConfig
from views.appearance.timer_view import TimerViewManager
from models.sound.sound_effect import TimerSoundEffect


class StopSignal(Exception):
    pass


class PomodoroTimer:
    def __init__(self, timer_config: TimerConfig, alarm_config: AlarmConfig, timer_view_manager: TimerViewManager,
                 change_ux_to_focus_mode, change_ux_to_break_mode) -> None:
        self.__timer_settings = timer_config.get_settings()
        self.__se = TimerSoundEffect(alarm_config)
        self.__timer_view_manager = timer_view_manager
        self.change_ux_to_focus_mode = change_ux_to_focus_mode
        self.change_ux_to_break_mode = change_ux_to_break_mode
        self.__remain_loop = 0
        self.__remain_minutes = 0
        self.__remain_seconds = 0
        self.__is_called_stopping_signal = False
        self.__on_pomodoro_process: bool = False
        self.__on_break: bool = True
        self.__thread: Optional[threading.Thread] = None

    def is_running(self) -> bool:
        return self.__thread is not None

    def on_pomodoro_process(self) -> bool:
        return self.__on_pomodoro_process

    def on_break(self) -> bool:
        return self.__on_break

    def apply_renewal_config(self, timer_config, alarm_config) -> None:
        updated_timer_settings = timer_config.get_settings()
        if self.__timer_settings != updated_timer_settings:
            self.__timer_settings = updated_timer_settings
        self.__se.apply_renewal_config(alarm_config)

    def update_minutes(self, minutes) -> None:
        self.__remain_minutes = minutes
        self.__timer_view_manager.update_displayed_minutes(self.__remain_minutes)

    def update_seconds(self, seconds) -> None:
        self.__remain_seconds = seconds
        self.__timer_view_manager.update_displayed_seconds(self.__remain_seconds)

    def update_remain_loop(self, remain_loop) -> None:
        self.__remain_loop = remain_loop
        self.__timer_view_manager.update_remain_loop_label(self.__remain_loop)

    def set_time(self, minutes, seconds) -> None:
        self.update_minutes(minutes)
        self.update_seconds(seconds)

    def countdown(self) -> None:
        for remain_minutes in range(self.__remain_minutes, -1, -1):
            self.update_minutes(remain_minutes)
            for remain_seconds in range(self.__remain_seconds, -1, -1):
                self.update_seconds(remain_seconds)
                if remain_minutes == 0:
                    if remain_seconds == 0:
                        return
                    elif remain_seconds <= 3:
                        self.__se.countdown_sound()
                time.sleep(1)
                if self.__is_called_stopping_signal:
                    raise StopSignal()
            self.__remain_seconds = 59

    def change_to_prepare_mode(self) -> None:
        count_minutes = self.__timer_settings["count_seconds"] // 60
        count_seconds = self.__timer_settings["count_seconds"] % 60
        self.set_time(count_minutes, count_seconds)

    def change_to_focus_mode(self) -> None:
        if self.__remain_loop == 0:
            self.update_remain_loop(self.__timer_settings["loop_times"])
        self.set_time(self.__timer_settings["task_minutes"], 0)
        self.__on_break = False
        self.change_ux_to_focus_mode()

    def change_to_break_mode(self) -> None:
        self.update_remain_loop(self.__remain_loop - 1)
        if self.__remain_loop >= 1:
            self.set_time(self.__timer_settings["short_break_minutes"], 0)
        else:
            self.set_time(self.__timer_settings["long_break_minutes"], 0)
        self.__on_break = True
        self.change_ux_to_break_mode()

    def switch_mode(self) -> None:
        if self.__on_break:
            self.change_to_focus_mode()
        else:
            self.change_to_break_mode()

    def continue_pomodoro_cycle(self) -> None:
        if self.__remain_minutes == 0 and self.__remain_seconds == 0:
            self.__se.play_alarm()
            self.switch_mode()
        try:
            self.countdown()
        except StopSignal:
            return
        self.continue_pomodoro_cycle()

    def start_pomodoro_process(self) -> None:
        self.__on_pomodoro_process = True
        self.update_remain_loop(self.__timer_settings["loop_times"])
        if self.__timer_settings["will_count"]:
            self.change_to_prepare_mode()
        self.continue_pomodoro_cycle()

    def start_timer(self) -> None:
        self.__is_called_stopping_signal = False
        if self.__on_pomodoro_process:
            self.__thread = Thread(target=self.continue_pomodoro_cycle)
        else:
            self.__thread = Thread(target=self.start_pomodoro_process)
        self.__thread.start()

    def stop_timer(self) -> None:
        self.__is_called_stopping_signal = True
        if self.__thread is not None:
            self.__thread.join()
            del self.__thread
            self.__thread = None

    def clear(self) -> None:
        self.stop_timer()
        self.set_time(0, 0)
        self.update_remain_loop(0)
        self.__on_pomodoro_process = False
        self.__on_break = True
