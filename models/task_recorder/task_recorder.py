from datetime import datetime
from typing import Final, Optional
from zoneinfo import ZoneInfo

from custom_types.task import TaskRecord, TaskRecordList
from models.configuration.config_class.task_recorder_config import TaskRecorderConfig
from models.task_recorder.file_parser import RecordFileParser


class DateTimeFormatter:
    def __init__(self):
        self.__time_determiner: Final[str] = ':'
        self.__seconds_per_hour: Final[int] = 3600
        self.__seconds_per_minute: Final[int] = 60

    def get_time_list(self, time_str: str) -> list[int]:
        if time_str in ('', '-'):
            return [0, 0, 0]
        time_list = list(map(int, time_str.split(self.__time_determiner)))
        if len(time_list) == 2:
            return [0] + time_list
        return time_list

    @staticmethod
    def calculate_difference_of_seconds(earlier_time: datetime, later_time: datetime) -> int:
        dif_time = later_time - earlier_time
        return dif_time.seconds

    def calculate_interval_seconds(self, earlier_time: str, later_time: str) -> int:
        earlier_time_list = self.get_time_list(earlier_time)
        later_time_list = self.get_time_list(later_time)
        hour_diff = later_time_list[0] - earlier_time_list[0]
        minute_diff = later_time_list[1] - earlier_time_list[1]
        second_diff = later_time_list[2] - earlier_time_list[2]
        dif_time = hour_diff * self.__seconds_per_hour + minute_diff * self.__seconds_per_minute + second_diff
        if dif_time < 0:
            return dif_time + 24 * self.__seconds_per_hour
        return dif_time

    def format_time_to_seconds(self, time_str: str) -> int:
        time_list = self.get_time_list(time_str)
        return time_list[0] * self.__seconds_per_hour + time_list[1] * self.__seconds_per_minute + time_list[2]

    def format_seconds_to_time(self, sec: int) -> str:
        m, s = divmod(sec, 60)
        h, m = divmod(m, 60)
        if h > 0:
            return str(h) + self.__time_determiner + str(m).zfill(2) + self.__time_determiner + str(s).zfill(2)
        return str(m) + self.__time_determiner + str(s).zfill(2)


class TaskRecorder:
    def __init__(self, task_recorder_config: TaskRecorderConfig) -> None:
        self.__settings = task_recorder_config.get_settings()
        self.__task_record: Final[TaskRecord] = {"タスク名": '', "開始時間": '', "終了時間": '', "実働時間": '', "休憩時間": ''}
        self.__file_parser = RecordFileParser(
            list(self.__task_record.keys()), self.__settings["file_format_index"], self.__settings["save_file_path"]
        )
        self.__datetime_formatter = DateTimeFormatter()
        self.__current_task_name = ""
        self.__start_time = None
        self.__interrupt_time = None
        self.__break_seconds = 0

    def set_task_name(self, task_name: str) -> None:
        if task_name == self.__current_task_name:
            return
        self.save_task_record()
        self.__current_task_name = task_name

    def apply_task_recorder_config(self, task_recorder_config: TaskRecorderConfig) -> None:
        updated_settings = task_recorder_config.get_settings()
        if updated_settings != self.__settings:
            self.__settings = updated_settings
            self.__file_parser.apply_settings(self.__settings["file_format_index"], self.__settings["save_file_path"])

    def timestump(self) -> Optional[datetime]:
        if not self.__settings["will_record_task"]:
            return None
        return datetime.now(ZoneInfo('Asia/Tokyo'))

    def start_task(self) -> None:
        current_time = self.timestump()
        if self.__start_time is None:
            self.__start_time = current_time
        if self.__interrupt_time is not None:
            self.count_break_seconds(current_time)

    def interrupt_task(self) -> None:
        self.__interrupt_time = self.timestump()

    def count_break_seconds(self, current_time: datetime) -> None:
        self.__break_seconds += self.__datetime_formatter.calculate_difference_of_seconds(
            self.__interrupt_time, current_time
        )
        self.__interrupt_time = None

    def calculate_actual_working_seconds(self, current_time: datetime) -> int:
        elapsed_seconds = self.__datetime_formatter.calculate_difference_of_seconds(self.__start_time, current_time)
        if self.__settings["will_record_break"]:
            return elapsed_seconds - self.__break_seconds
        return elapsed_seconds

    def get_new_task_record(self, task_name: str, start_time: str, finish_time: str, working_seconds: int,
                            break_seconds: int) -> TaskRecord:
        task_record = self.__task_record.copy()
        task_record['タスク名'] = task_name
        task_record['開始時間'] = start_time
        task_record['終了時間'] = finish_time
        task_record['実働時間'] = self.__datetime_formatter.format_seconds_to_time(working_seconds)
        task_record['休憩時間'] = self.__datetime_formatter.format_seconds_to_time(break_seconds) \
            if self.__settings["will_record_break"] else "-"
        return task_record

    def calculate_interval_seconds(self, previous_task_record: TaskRecord,
                                   current_task_data: TaskRecord) -> int:
        return self.__datetime_formatter.calculate_interval_seconds(
            previous_task_record['終了時間'], current_task_data['開始時間']
        )

    def integrate_task_record(self, previous_task_record: TaskRecord, current_task_data: TaskRecord,
                              interval_seconds: int) -> TaskRecord:
        working_seconds = self.__datetime_formatter.format_time_to_seconds(previous_task_record['実働時間']) + \
                          self.__datetime_formatter.format_time_to_seconds(current_task_data['実働時間'])
        break_seconds = \
            self.__datetime_formatter.format_time_to_seconds(previous_task_record['休憩時間']) + \
            self.__datetime_formatter.format_time_to_seconds(current_task_data['休憩時間']) + \
            interval_seconds

        integrated_task_record = self.get_new_task_record(
            previous_task_record['タスク名'], previous_task_record['開始時間'], current_task_data['終了時間'],
            working_seconds, break_seconds
        )

        return integrated_task_record

    def get_current_task_data(self, current_time: datetime) -> TaskRecord:
        actual_working_seconds = self.calculate_actual_working_seconds(current_time)
        task_name = '未設定タスク' if self.__current_task_name == "" else self.__current_task_name
        stocking_task_record = self.get_new_task_record(task_name, self.__start_time.time().strftime('%X'),
                                                        current_time.time().strftime('%X'), actual_working_seconds,
                                                        self.__break_seconds)
        return stocking_task_record

    def integrate_task_record_list(self, previous_task_record: TaskRecordList,
                                   current_task_data: TaskRecord) -> TaskRecordList:
        previous_total_working_seconds, previous_total_break_seconds = 0, 0
        integrated_task_record_list = []

        if not previous_task_record:
            integrated_task_record_list += [current_task_data]
        else:
            previous_total_task_record = previous_task_record[-1]
            last_task_record = previous_task_record[-2]
            previous_total_working_seconds = self.__datetime_formatter.format_time_to_seconds(
                previous_total_task_record['実働時間']
            )
            previous_total_break_seconds = self.__datetime_formatter.format_time_to_seconds(
                previous_total_task_record['休憩時間']
            )
            if last_task_record['タスク名'] == current_task_data['タスク名']:
                interval_seconds = self.calculate_interval_seconds(last_task_record, current_task_data)
                integrated_task_record = self.integrate_task_record(last_task_record, current_task_data,
                                                                    interval_seconds)
                previous_total_break_seconds += interval_seconds
                integrated_task_record_list = previous_task_record[:-2] + [integrated_task_record]
            else:
                integrated_task_record_list = previous_task_record[:-1] + [current_task_data]

        previous_total_working_seconds += self.__datetime_formatter.format_time_to_seconds(current_task_data['実働時間'])
        previous_total_break_seconds += self.__datetime_formatter.format_time_to_seconds(current_task_data['休憩時間'])
        
        total_task_record = self.get_new_task_record('合計', integrated_task_record_list[0]['開始時間'],
                                                     integrated_task_record_list[-1]['終了時間'],
                                                     previous_total_working_seconds, previous_total_break_seconds)

        return integrated_task_record_list + [total_task_record]

    def save_task_record(self) -> None:
        if self.__start_time is None or not self.__settings["will_record_task"]:
            return
        year = self.__start_time.strftime('%Y')
        year_and_month = f"{year}/{self.__start_time.strftime('%-m')}"
        day_on_a_week = self.__start_time.strftime('%-d(%a)')
        current_time = self.timestump()
        if self.__interrupt_time is not None:
            self.count_break_seconds(current_time)
        current_task_data = self.get_current_task_data(current_time)
        self.__start_time = None
        self.__break_seconds = 0
        previous_task_record = self.__file_parser.get_previous_task_record(year_and_month, day_on_a_week)
        integrated_task_record = self.integrate_task_record_list(previous_task_record, current_task_data)
        self.__file_parser.save_task_record(year_and_month, day_on_a_week, integrated_task_record)
        self.__file_parser.remove_duplicated_directory(year)
