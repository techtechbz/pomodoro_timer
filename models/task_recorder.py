import csv
from datetime import datetime
from enum import Enum
import os
import shutil
from typing import Final
from zoneinfo import ZoneInfo


class FileFormat(Enum):
    csv = 0
    markdown = 1
    両方 = 2

    @classmethod
    def get_file_format_list(cls):
        return list(map(lambda member: member.name, cls))


class RecordCsvParser:
    def __init__(self, header_list):
        self.__extension: Final[str] = ".csv"
        self.__header_list = header_list

    def get_previous_task_record(self, read_file_path_without_extension):
        path = read_file_path_without_extension + self.__extension
        if not os.path.isfile(path):
            return []

        with open(path, 'r', encoding="UTF-8") as f:
            reader = csv.DictReader(f)
            record = list(reader)

        return record

    def save_task_record(self, save_file_path_without_extension: str, task_record):
        path = save_file_path_without_extension + self.__extension
        with open(path, 'w', newline='', encoding='UTF-8') as f:
            writer = csv.DictWriter(f, self.__header_list)
            writer.writeheader()
            writer.writerows(task_record)


class RecordMarkdownParser:
    def __init__(self, header_list):
        self.__extension = ".md"
        self.__header_list = header_list
        self.__line_break = '\n'
        self.__header_delimiter = '-------'
        self.__item_delimiter = '|'

    def format_row_sequence(self, item_list):
        return self.__item_delimiter + self.__item_delimiter.join(item_list) + self.__item_delimiter

    def get_previous_task_record(self, read_file_path_without_extension):
        path = read_file_path_without_extension + self.__extension
        if not os.path.isfile(path):
            return []

        record = []
        with open(path, 'r', encoding="UTF-8") as f:
            for line in f.readlines():
                # 始端と終端に格納されている空の文字列を削除
                item_list = line.split(self.__item_delimiter)[1:-1]
                if len(item_list) != len(self.__header_list):
                    continue
                data = {header: item for header, item in zip(self.__header_list, item_list)
                        if header != item and self.__header_delimiter not in item}
                if data != {}:
                    record += [data]
        return record

    def save_task_record(self, save_file_path_without_extension, task_record):
        path = save_file_path_without_extension + self.__extension
        with open(path, 'w', encoding='UTF-8') as f:
            print(self.format_row_sequence(self.__header_list), file=f)
            print(self.format_row_sequence([self.__header_delimiter for _ in self.__header_list]), file=f)
            for record in task_record:
                print(self.format_row_sequence([record[header] for header in self.__header_list]), file=f)


class RecordFileParser:
    def __init__(self, file_format_index: int, path: str) -> None:
        self.__file_format = FileFormat(file_format_index)
        self.__read_file_path = path
        self.__save_file_path = path
        self.__header_list = ["タスク名", "開始時間", "終了時間", "実働時間", "休憩時間"]
        self.__csv_parser = RecordCsvParser(self.__header_list)
        self.__markdown_parser = RecordMarkdownParser(self.__header_list)

    def apply_settings(self, file_format_index: int, path: str):
        self.__file_format = FileFormat(file_format_index)
        self.__save_file_path = path
        if self.__read_file_path == "":
            self.__read_file_path = path

    def get_previous_task_record(self, read_file_path_without_extension: str):
        csv_record = self.__csv_parser.get_previous_task_record(read_file_path_without_extension)
        markdown_record = self.__markdown_parser.get_previous_task_record(read_file_path_without_extension)
        if len(csv_record) >= len(markdown_record):
            return csv_record
        return markdown_record

    def integrate_task_record(self, year_and_month, day_on_a_week, task_record):
        read_file_path_without_extension = f'{self.__read_file_path}/{year_and_month}/{day_on_a_week}/{day_on_a_week}'
        return self.get_previous_task_record(read_file_path_without_extension) + task_record

    def save_task_record(self, year_and_month, day_on_a_week, task_record) -> None:
        # get total task record
        total_task_record = self.integrate_task_record(year_and_month, day_on_a_week, task_record)

        # create new directory
        save_directory = f'{self.__save_file_path}/{year_and_month}/{day_on_a_week}'
        if not os.path.isdir(save_directory):
            os.makedirs(save_directory)

        save_file_path_without_extension = f'{save_directory}/{day_on_a_week}'

        if self.__file_format == FileFormat.csv:
            self.__csv_parser.save_task_record(save_file_path_without_extension, total_task_record)
        elif self.__file_format == FileFormat.markdown:
            self.__markdown_parser.save_task_record(save_file_path_without_extension, total_task_record)
        else:
            self.__csv_parser.save_task_record(save_file_path_without_extension, total_task_record)
            self.__markdown_parser.save_task_record(save_file_path_without_extension, total_task_record)

    def remove_duplicated_directory(self, year: int) -> None:
        if self.__read_file_path != self.__save_file_path:
            shutil.rmtree(f'{self.__read_file_path}/{year}')
            self.__read_file_path = self.__save_file_path


class TaskRecorder:
    def __init__(self, task_recorder_config) -> None:
        self.__settings = task_recorder_config.get_settings()
        self.__file_parser = RecordFileParser(self.__settings["file_format_index"], self.__settings["save_file_path"])
        self.__current_task_name = ""
        self.__start_time = None
        self.__interrupt_time = None
        self.__break_seconds = 0
        self.__task_record = []

    def get_current_task_name(self) -> str:
        return self.__current_task_name

    def set_task_name(self, task_name: str) -> None:
        if self.__start_time is not None:
            self.stock_task_data()
        self.__current_task_name = task_name

    def apply_task_recorder_config(self, task_recorder_config) -> None:
        updated_settings = task_recorder_config.get_settings()
        if updated_settings != self.__settings:
            self.__settings = updated_settings
            self.__file_parser.apply_settings(self.__settings["file_format_index"], self.__settings["save_file_path"])

    def timestump(self):
        if not self.__settings["will_record_task"]:
            return None
        return datetime.now(ZoneInfo('Asia/Tokyo'))

    @staticmethod
    def calculate_difference_of_seconds(earlier_time, later_time):
        dif_time = later_time - earlier_time
        return dif_time.seconds

    def start_task(self) -> None:
        current_time = self.timestump()
        if self.__start_time is None:
            self.__start_time = current_time
        if self.__interrupt_time is not None:
            self.count_break_seconds(current_time)

    def interrupt_task(self) -> None:
        self.__interrupt_time = self.timestump()

    def count_break_seconds(self, current_time) -> None:
        self.__break_seconds += self.calculate_difference_of_seconds(self.__interrupt_time, current_time)
        self.__interrupt_time = None

    def calculate_actual_working_seconds(self, current_time):
        elapsed_seconds = self.calculate_difference_of_seconds(self.__start_time, current_time)
        if self.__settings["will_record_break"]:
            return elapsed_seconds - self.__break_seconds
        return elapsed_seconds

    @staticmethod
    def format_seconds_to_time(sec: int) -> str:
        m, s = divmod(sec, 60)
        h, m = divmod(m, 60)
        if h > 0:
            return f'{h}:{str(m).zfill(2)}:{str(s).zfill(2)}'
        return f'{m}:{str(s).zfill(2)}'

    def stock_task_data(self) -> None:
        current_time = self.timestump()
        if self.__interrupt_time is not None:
            self.count_break_seconds(current_time)
        self.__task_record += [{
            "タスク名": '未設定タスク' if self.__current_task_name == "" else self.__current_task_name,
            "開始時間": self.__start_time.time().strftime('%X'),
            "終了時間": current_time.time().strftime('%X'),
            "実働時間": self.format_seconds_to_time(self.calculate_actual_working_seconds(current_time)),
            "休憩時間": self.format_seconds_to_time(self.__break_seconds) if self.__settings["will_record_break"] else "-",
        }]
        self.__start_time = None
        self.__break_seconds = 0

    def save_task_record(self) -> None:
        if self.__start_time is None or not self.__settings["will_record_task"]:
            return
        year = self.__start_time.strftime('%Y')
        year_and_month = f"{year}/{self.__start_time.strftime('%-m')}"
        day_on_a_week = self.__start_time.strftime('%-d(%a)')
        self.stock_task_data()
        self.__file_parser.save_task_record(year_and_month, day_on_a_week, self.__task_record)
        self.__file_parser.remove_duplicated_directory(year)
        self.__task_record = []
