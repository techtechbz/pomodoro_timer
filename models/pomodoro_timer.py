import time

from models.sound.sound_effect import TimerSoundEffect
from threading import Thread


class StopSignal(Exception):
    pass


class PomodoroTimer:
    def __init__(self, timer_config, alarm_config, update_displayed_minutes, update_displayed_seconds,
                 update_remain_loop_label, set_ux_for_focus_mode, set_ux_for_break_mode):
        self.__timer_settings = timer_config.get_settings()
        self.__se = TimerSoundEffect(alarm_config)
        self.update_displayed_minutes = update_displayed_minutes
        self.update_displayed_seconds = update_displayed_seconds
        self.update_remain_loop_label = update_remain_loop_label
        self.set_ux_for_focus_mode = set_ux_for_focus_mode
        self.set_ux_for_break_mode = set_ux_for_break_mode
        self.__remain_loop = 0
        self.__remain_minutes = 0
        self.__remain_seconds = 0
        self.__is_called_stopping_signal = False
        self.__on_pomodoro_process = False
        self.__on_break = True
        self.__thread = None

    def is_running(self):
        return self.__thread is not None

    def on_pomodoro_process(self):
        return self.__on_pomodoro_process

    def on_break(self):
        return self.__on_break

    def apply_renewal_config(self, timer_config, alarm_config):
        updated_timer_settings = timer_config.get_settings()
        if self.__timer_settings != updated_timer_settings:
            self.__timer_settings = updated_timer_settings
        self.__se.apply_renewal_config(alarm_config)

    def update_minutes(self, minutes):
        self.__remain_minutes = minutes
        self.update_displayed_minutes(self.__remain_minutes)

    def update_seconds(self, seconds):
        self.__remain_seconds = seconds
        self.update_displayed_seconds(self.__remain_seconds)

    def update_remain_loop(self, remain_loop):
        self.__remain_loop = remain_loop
        self.update_remain_loop_label(self.__remain_loop)

    def set_time(self, minutes, seconds):
        self.update_minutes(minutes)
        self.update_seconds(seconds)

    def countdown(self):
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

    def change_to_prepare_mode(self):
        count_minutes = self.__timer_settings["count_seconds"] // 60
        count_seconds = self.__timer_settings["count_seconds"] % 60
        self.set_time(count_minutes, count_seconds)

    def change_to_focus_mode(self):
        if self.__remain_loop == 0:
            self.update_remain_loop(self.__timer_settings["loop_times"])
        self.set_time(self.__timer_settings["task_minutes"], 0)
        self.__on_break = False
        self.set_ux_for_focus_mode()

    def change_to_break_mode(self):
        self.update_remain_loop(self.__remain_loop - 1)
        if self.__remain_loop >= 1:
            self.set_time(self.__timer_settings["short_break_minutes"], 0)
        else:
            self.set_time(self.__timer_settings["long_break_minutes"], 0)
        self.__on_break = True
        self.set_ux_for_break_mode()

    def switch_mode(self):
        if self.__on_break:
            self.change_to_focus_mode()
        else:
            self.change_to_break_mode()

    def continue_pomodoro_cycle(self):
        if self.__remain_minutes == 0 and self.__remain_seconds == 0:
            self.__se.play_alarm()
            self.switch_mode()
        try:
            self.countdown()
        except StopSignal:
            return
        self.continue_pomodoro_cycle()

    def start_pomodoro_process(self):
        self.__on_pomodoro_process = True
        self.update_remain_loop(self.__timer_settings["loop_times"])
        if self.__timer_settings["will_count"]:
            self.change_to_prepare_mode()
        self.continue_pomodoro_cycle()

    def start_timer(self):
        self.__is_called_stopping_signal = False
        if self.__on_pomodoro_process:
            self.__thread = Thread(target=self.continue_pomodoro_cycle)
        else:
            self.__thread = Thread(target=self.start_pomodoro_process)
        self.__thread.start()

    def stop_timer(self):
        self.__is_called_stopping_signal = True
        if self.__thread is not None:
            self.__thread.join()
            del self.__thread
            self.__thread = None

    def clear(self):
        self.stop_timer()
        self.set_time(0, 0)
        self.update_remain_loop(0)
        self.__on_pomodoro_process = False
        self.__on_break = True
