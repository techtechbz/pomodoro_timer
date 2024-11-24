from typing import Literal, TypedDict

FileExtension = Literal[".md", ".csv"]
TaskRecord = TypedDict('TaskRecord', {"タスク名": str, "開始時間": str, "終了時間": str, "実働時間": str, "休憩時間": str})
TaskRecordList = list[TaskRecord]
