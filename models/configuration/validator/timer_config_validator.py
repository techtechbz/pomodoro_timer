from typing import Optional

from models.configuration.validator.validation_status import ValidationStatus


class TimerConfigValidator:
    def __init__(self) -> None:
        self.__partial_status = ValidationStatus.unverified
        self.__status = ValidationStatus.unverified
        self.__message = ""

    def preset_name_validator(self, preset_num: int, input_name: str) -> Optional[str]:
        input_len = len(input_name)
        if 1 <= input_len <= 50:
            return input_name
        if self.__partial_status.value <= 3:
            self.__partial_status = ValidationStatus.error
        if self.__message != "":
            self.__message += "\n"
        self.__message += f"プリセット名(プリセット{preset_num}): 1~50文字以内で入力してください。"
        return None

    def input_value_validator(self, field_name: str, input_value: str, max_value: int, will_warn=False) \
            -> Optional[int]:
        try:
            value = int(input_value)
            if not all((value >= 1, value <= max_value)):
                raise ValueError()
            return value
        except ValueError:
            if self.__partial_status.value <= 3:
                self.__partial_status = ValidationStatus.warning if will_warn else ValidationStatus.error
            if self.__message != "":
                self.__message += "\n"
            self.__message += f'・{field_name}: 1~{max_value}までの数字で指定してください。'
            return None

    def update_status(self) -> None:
        if self.__partial_status.value > self.__status.value:
            self.__status = self.__partial_status
        self.__partial_status = ValidationStatus.unverified

    def validation(self, inputs_list):
        self.__partial_status = ValidationStatus.unverified
        self.__status = ValidationStatus.unverified
        self.__message = ""
        timer_settings_list = []
        for i, inputs in enumerate(inputs_list):
            preset_num = i + 1
            validated_preset_name: str = self.preset_name_validator(preset_num, inputs["preset_name"])
            validated_task_minutes: int = self.input_value_validator(f"タスク時間(分)(プリセット{preset_num})",
                                                                     inputs["task_minutes"], 300)
            validated_short_break_minutes: int = self.input_value_validator(f"小休憩時間(分)(プリセット{preset_num})",
                                                                            inputs["short_break_minutes"], 60)
            validated_long_break_minutes: int = self.input_value_validator(f"長休憩時間(分)(プリセット{preset_num})",
                                                                           inputs["long_break_minutes"], 300)
            validated_loop_times: int = self.input_value_validator(f"ループ回数(回)(プリセット{preset_num})",
                                                                   inputs["loop_times"], 10)
            validated_will_count = inputs["will_count"]
            validated_count_seconds: int = self.input_value_validator(f"カウント秒(秒)(プリセット{preset_num})",
                                                                      inputs["count_seconds"], 300,
                                                                      will_warn=not validated_will_count)
            timer_settings_list.append({
                "preset_name": validated_preset_name,
                "task_minutes": validated_task_minutes,
                "short_break_minutes": validated_short_break_minutes,
                "long_break_minutes": validated_long_break_minutes,
                "loop_times": validated_loop_times,
                "will_count": validated_will_count,
                "count_seconds": validated_count_seconds
            })

            self.update_status()

        if self.__status == ValidationStatus.unverified:
            self.__status = ValidationStatus.success

        return timer_settings_list

    def return_validation_result(self):
        return self.__status, self.__message

    def is_valid_settings(self) -> bool:
        return self.__status == ValidationStatus.success
