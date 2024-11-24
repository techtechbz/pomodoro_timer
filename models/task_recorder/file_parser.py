from enum import Enum
import csv
import os
import shutil
from typing import Final

from custom_types.task import FileExtension, TaskRecordList


class FileFormat(Enum):
    csv = 0
    markdown = 1
    両方 = 2

    @classmethod
    def get_file_format_list(cls) -> list[str]:
        return list(map(lambda member: member.name, cls))


class RecordCsvParser:
    def __init__(self, header_list: list[str]) -> None:
        self.__extension: Final[FileExtension] = ".csv"
        self.__header_list: Final[list[str]] = header_list

    def get_previous_task_record(self, read_file_path_without_extension: str) -> TaskRecordList:
        path = read_file_path_without_extension + self.__extension
        if not os.path.isfile(path):
            return []

        with open(path, 'r', encoding="UTF-8") as f:
            reader = csv.DictReader(f)
            record = list(reader)

        return record

    def save_task_record(self, save_file_path_without_extension: str, task_record_list: TaskRecordList) -> None:
        path = save_file_path_without_extension + self.__extension
        with open(path, 'w', newline='', encoding='UTF-8') as f:
            writer = csv.DictWriter(f, self.__header_list)
            writer.writeheader()
            writer.writerows(task_record_list)


class RecordMarkdownParser:
    def __init__(self, header_list: list[str]) -> None:
        self.__extension: Final[FileExtension] = ".md"
        self.__header_list: Final[list[str]] = header_list
        self.__line_break: Final[str] = '\n'
        self.__header_delimiter: Final[str] = '-------'
        self.__item_delimiter: Final[str] = '|'

    def format_row_sequence(self, item_list: list[str]) -> str:
        return self.__item_delimiter + self.__item_delimiter.join(item_list) + self.__item_delimiter

    def get_previous_task_record(self, read_file_path_without_extension: str) -> list[dict[str, str]]:
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

    def save_task_record(self, save_file_path_without_extension: str, task_record_list: TaskRecordList) -> None:
        path = save_file_path_without_extension + self.__extension
        with open(path, 'w', encoding='UTF-8') as f:
            print(self.format_row_sequence(self.__header_list), file=f)
            print(self.format_row_sequence([self.__header_delimiter for _ in self.__header_list]), file=f)
            for record in task_record_list:
                print(self.format_row_sequence([record[header] for header in self.__header_list]), file=f)


class RecordFileParser:
    def __init__(self, header_list: list[str], file_format_index: int, path: str) -> None:
        self.__header_list: Final[list[str]] = header_list
        self.__csv_parser: Final[RecordCsvParser] = RecordCsvParser(self.__header_list)
        self.__markdown_parser: Final[RecordMarkdownParser] = RecordMarkdownParser(self.__header_list)
        self.__file_format: FileFormat = FileFormat(file_format_index)
        self.__read_file_path: str = path
        self.__save_file_path: str = path

    def apply_settings(self, file_format_index: int, path: str) -> None:
        self.__file_format: FileFormat = FileFormat(file_format_index)
        self.__save_file_path = path
        if self.__read_file_path == "":
            self.__read_file_path = path

    def get_previous_task_record(self, year_and_month: str, day_on_a_week: str) -> TaskRecordList:
        read_file_path_without_extension = f'{self.__read_file_path}/{year_and_month}/{day_on_a_week}/{day_on_a_week}'
        csv_record = self.__csv_parser.get_previous_task_record(read_file_path_without_extension)
        markdown_record = self.__markdown_parser.get_previous_task_record(read_file_path_without_extension)
        if len(csv_record) >= len(markdown_record):
            return csv_record
        return markdown_record

    def save_task_record(self, year_and_month: str, day_on_a_week: str,
                         task_record_list: TaskRecordList) -> None:
        # create new directory
        save_directory = f'{self.__save_file_path}/{year_and_month}/{day_on_a_week}'
        if not os.path.isdir(save_directory):
            os.makedirs(save_directory)

        save_file_path_without_extension = f'{save_directory}/{day_on_a_week}'

        if self.__file_format == FileFormat.csv:
            self.__csv_parser.save_task_record(save_file_path_without_extension, task_record_list)
        elif self.__file_format == FileFormat.markdown:
            self.__markdown_parser.save_task_record(save_file_path_without_extension, task_record_list)
        else:
            self.__csv_parser.save_task_record(save_file_path_without_extension, task_record_list)
            self.__markdown_parser.save_task_record(save_file_path_without_extension, task_record_list)

    def remove_duplicated_directory(self, year: int) -> None:
        if self.__read_file_path != self.__save_file_path:
            shutil.rmtree(f'{self.__read_file_path}/{year}')
            self.__read_file_path = self.__save_file_path
