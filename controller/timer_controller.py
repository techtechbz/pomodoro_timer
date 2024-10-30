from sound import play_effect

from models.pomodoro_timer import PomodoroTimer
from views.appearance.timer_view import TimerViewManager


class TimerController:
    def __init__(self, timer_config, alarm_config, show_validation_error_message, set_ux_for_focus_mode,
                 set_ux_for_break_mode, reset_ux, start_task, interrupt_task):
        self.__timer_view_manager = TimerViewManager()
        if timer_config is None:
            self.show_validation_error_message = show_validation_error_message
            return

        self.__timer = PomodoroTimer(timer_config=timer_config,
                                     alarm_config=alarm_config,
                                     update_displayed_minutes=self.__timer_view_manager.update_displayed_minutes,
                                     update_displayed_seconds=self.__timer_view_manager.update_displayed_seconds,
                                     update_remain_loop_label=self.__timer_view_manager.update_remain_loop_label,
                                     set_ux_for_focus_mode=set_ux_for_focus_mode,
                                     set_ux_for_break_mode=set_ux_for_break_mode)
        self.reset_ux = reset_ux
        self.start_task = start_task
        self.interrupt_task = interrupt_task
        self.__timer_view_manager.set_button_action(self.play_timer, self.clear_timer)

    def get_timer_view_instance(self):
        return self.__timer_view_manager.get_view_instance()

    def apply_renewal_config(self, timer_config, alarm_config) -> None:
        self.reset()
        self.__timer.apply_renewal_config(timer_config, alarm_config)

    def execute_command(self, sender) -> None:
        if sender['title'] == 'play':
            self.play_timer()
        if sender['title'] == 'clear':
            self.clear_timer()

    @staticmethod
    def effect_pushing_button_sound():
        play_effect('ui:switch33')

    def start_timer(self):
        self.__timer_view_manager.change_play_timer_button_title("STOP")
        self.__timer.start_timer()
        self.start_task(self.__timer.on_break())

    def stop_timer(self):
        self.__timer.stop_timer()
        self.__timer_view_manager.change_play_timer_button_title("START")
        self.interrupt_task()

    def play_timer(self, _=None):
        self.effect_pushing_button_sound()
        if self.__timer is None:
            self.show_validation_error_message()
            return
        if self.__timer.is_running():
            self.stop_timer()
        else:
            self.start_timer()

    def reset(self):
        if self.__timer is not None:
            self.__timer.clear()
            self.stop_timer()
            self.reset_ux()

    def clear_timer(self, _=None):
        self.effect_pushing_button_sound()
        self.reset()
