from custom_types.settings import TaskRecorderSettings


class TaskRecorderConfig:
    def __init__(self, will_record_task: bool, will_record_break: bool, file_format_index: int,
                 save_file_path: str) -> None:
        self.__will_record_task = will_record_task
        self.__will_record_break = will_record_break
        self.__file_format_index = file_format_index
        self.__save_file_path = save_file_path

    def get_settings(self) -> TaskRecorderSettings:
        return {"will_record_task": self.__will_record_task,
                "will_record_break": self.__will_record_break,
                "file_format_index": self.__file_format_index,
                "save_file_path": self.__save_file_path}
