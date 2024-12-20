from custom_types.settings import TimerSettings


class TimerConfig:
    def __init__(self, preset_name: str, task_minutes: int, short_break_minutes: int, long_break_minutes: int,
                 loop_times: int, will_count: bool, count_seconds: int) -> None:
        self.__preset_name = preset_name
        self.__task_minutes = task_minutes
        self.__short_break_minutes = short_break_minutes
        self.__long_break_minutes = long_break_minutes
        self.__loop_times = loop_times
        self.__will_count = will_count
        self.__count_seconds = count_seconds

    def get_preset_name(self) -> str:
        return self.__preset_name

    def get_settings(self) -> TimerSettings:
        return {"preset_name": self.__preset_name,
                "task_minutes": self.__task_minutes,
                "short_break_minutes": self.__short_break_minutes,
                "long_break_minutes": self.__long_break_minutes,
                "loop_times": self.__loop_times,
                "will_count": self.__will_count,
                "count_seconds": self.__count_seconds}
