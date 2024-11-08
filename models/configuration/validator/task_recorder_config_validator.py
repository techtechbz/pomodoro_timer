import os

from models.task_recorder.file_parser import FileFormat
from models.configuration.validator.validation_status import ValidationStatus


class TaskRecorderConfigValidator:
    def __init__(self):
        self.__partical_status = ValidationStatus.unverified
        self.__status = ValidationStatus.unverified
        self.__message = ""

    def file_path_validation(self, save_file_path):
        if save_file_path == "":
            self.__message = "・ディレクトリ: ディレクトリが指定されていません。"
            self.__status = ValidationStatus.error
        elif not os.path.isdir(save_file_path):
            self.__message = "・ディレクトリ: ディレクトリが見つかりませんでした。"
            self.__status = ValidationStatus.error

    def file_format_index_validation(self, file_format_index):
        try:
            _ = FileFormat(file_format_index)
        except ValueError:
            self.__message = "・ファイル形式: 不正な値です"
            self.__status = ValidationStatus.error

    def validation(self, will_record_task, will_record_break, file_format_index, save_file_path):
        self.__status = ValidationStatus.unverified
        self.__message = ""
        if will_record_task:
            self.file_path_validation(save_file_path)

        if self.__status == ValidationStatus.unverified:
            self.__status = ValidationStatus.success

        return {"will_record_task": will_record_task,
                "will_record_break": will_record_break,
                "file_format_index": file_format_index,
                "save_file_path": save_file_path}

    def return_validation_result(self):
        return self.__status, self.__message

    def is_valid_settings(self):
        return self.__status == ValidationStatus.success
