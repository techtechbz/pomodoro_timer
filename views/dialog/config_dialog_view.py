from enum import Enum
import math
import ui
from typing import Final, Optional

from custom_types.settings import AppSettingsInputs
from models.configuration.config_class.app_config import AppConfig
from models.configuration.default_settings import DefaultSettings
from views.config_menu.timer_config_menu_handler import TimerConfigMenuHandler
from views.config_menu.task_recorder_config_menu_handler import TaskRecorderConfigMenuHandler
from views.config_menu.alarm_config_menu_handler import AlarmConfigMenuHandler
from views.config_menu.music_player_config_menu_handler import MusicPlayerConfigMenuHandler


class ConfigurationItem(Enum):
    タイマー = 0
    タスク = 1
    アラーム = 2
    音楽 = 3

    @classmethod
    def get_configuration_item_list(cls):
        return list(map(lambda member: member.name, cls))


class ScrollMenuHandler:
    def __init__(self, config: Optional[AppConfig]) -> None:
        self.__default_settings: Final[DefaultSettings] = DefaultSettings()
        if config is None:
            all_settings = self.__default_settings.get_default_settings()
        else:
            all_settings = config.get_all_settings()
        preset_index = all_settings["preset_index_settings"]["preset_index"]
        self.__timer_config_menu_handler: Final[TimerConfigMenuHandler] = TimerConfigMenuHandler(
            preset_index, all_settings["timer_settings_list"]
        )
        self.__task_recorder_config_menu_handler: Final[TaskRecorderConfigMenuHandler] = \
            TaskRecorderConfigMenuHandler(all_settings["task_recorder_settings"])
        self.__alarm_config_menu_handler: Final[AlarmConfigMenuHandler] = \
            AlarmConfigMenuHandler(all_settings["alarm_settings"])
        self.__music_player_config_menu_handler: Final[MusicPlayerConfigMenuHandler] = \
            MusicPlayerConfigMenuHandler(all_settings["music_player_settings"])
        self.__current_menu_handler = self.__timer_config_menu_handler
        self.__current_menu_handler.insert_field_text()

    def change_current_menu_handler(self, configuration_item: ConfigurationItem) -> None:
        self.__current_menu_handler.write_out_field_inputs()
        if configuration_item == ConfigurationItem.タイマー:
            self.__timer_config_menu_handler.insert_field_text()
            self.__current_menu_handler = self.__timer_config_menu_handler
        elif configuration_item == ConfigurationItem.タスク:
            self.__task_recorder_config_menu_handler.insert_field_text()
            self.__current_menu_handler = self.__task_recorder_config_menu_handler
        elif configuration_item == ConfigurationItem.アラーム:
            self.__alarm_config_menu_handler.insert_field_text()
            self.__current_menu_handler = self.__alarm_config_menu_handler
        else:
            self.__music_player_config_menu_handler.insert_field_text()
            self.__current_menu_handler = self.__music_player_config_menu_handler

    def get_scroll_menu_view_instance(self) -> ui.View:
        return self.__current_menu_handler.get_view_instance()

    def get_scroll_view_size(self, extension=0) -> tuple[float, float]:
        scroll_menu_instance = self.get_scroll_menu_view_instance()
        return scroll_menu_instance.width, scroll_menu_instance.height + extension

    def get_all_setting_values(self) -> AppSettingsInputs:
        self.__current_menu_handler.write_out_field_inputs()
        preset_index, timer_settings_list = self.__timer_config_menu_handler.get_setting_values()
        task_recorder_settings = self.__task_recorder_config_menu_handler.get_setting_values()
        alarm_settings = self.__alarm_config_menu_handler.get_setting_values()
        music_player_settings = self.__music_player_config_menu_handler.get_setting_values()
        return {
            "preset_index_settings": {"preset_index": preset_index},
            "timer_settings_list": timer_settings_list,
            "task_recorder_settings": task_recorder_settings,
            "alarm_settings": alarm_settings,
            "music_player_settings": music_player_settings
        }

    def set_default_settings_inputs(self) -> None:
        default_settings = self.__default_settings.get_default_settings()
        self.__timer_config_menu_handler.reset_settings(default_settings["preset_index_settings"]["preset_index"],
                                                        default_settings["timer_settings_list"])
        self.__task_recorder_config_menu_handler.reset_settings(default_settings["task_recorder_settings"])
        self.__alarm_config_menu_handler.reset_settings(default_settings["alarm_settings"])
        self.__music_player_config_menu_handler.reset_settings(default_settings["music_player_settings"])

    @staticmethod
    def switch_subview_enabled(subview: ui.View, will_enabled: bool) -> None:
        if hasattr(subview, 'enabled'):
            subview.enabled = will_enabled
        elif hasattr(subview, 'touch_enabled'):
            subview.touch_enabled = will_enabled

    def switch_view_enabled(self, will_enabled: bool) -> None:
        if self.__current_menu_handler == self.__music_player_config_menu_handler:
            self.__music_player_config_menu_handler.switch_enabled(will_enabled)
        for subview in self.get_scroll_menu_view_instance().subviews:
            self.switch_subview_enabled(subview, will_enabled)


class ConfigDialogViewManager:
    def __init__(self, config: Optional[AppConfig]) -> None:
        self.__view_instance = ui.load_view("./pyui/dialog/config_dialog.pyui")
        self.__scroll_menu_handler = ScrollMenuHandler(config)
        self.__scale_factor = 1
        self.initiate_segmented_control()
        self.__view_instance["select_item_segmented_control"].action = self.swipe_scroll_config_menu

    def get_view_instance(self) -> ui.View:
        return self.__view_instance

    def set_scroll_config_menu(self, configuration_item: ConfigurationItem) -> None:
        self.__scroll_menu_handler.change_current_menu_handler(configuration_item)
        self.__view_instance["config_menu_scroll"].content_size = self.__scroll_menu_handler.get_scroll_view_size()
        self.__view_instance["config_menu_scroll"].add_subview(
            self.__scroll_menu_handler.get_scroll_menu_view_instance()
        )

    def initiate_segmented_control(self) -> None:
        initial_configuration_item = ConfigurationItem.タイマー
        self.__view_instance["select_item_segmented_control"].segments = ConfigurationItem.get_configuration_item_list()
        self.__view_instance["select_item_segmented_control"].selected_index = initial_configuration_item.value
        self.set_scroll_config_menu(initial_configuration_item)

    def swipe_scroll_config_menu(self, _=None) -> None:
        self.__view_instance["config_menu_scroll"].remove_subview(
            self.__scroll_menu_handler.get_scroll_menu_view_instance()
        )
        config_item_index = self.__view_instance["select_item_segmented_control"].selected_index
        self.set_scroll_config_menu(ConfigurationItem(config_item_index))

    def set_default_settings_inputs(self) -> None:
        self.__scroll_menu_handler.set_default_settings_inputs()

    def get_scale_factor(self, frame_height: float) -> float:
        return frame_height / self.__view_instance.height * 0.8

    def sizing(self, frame_width: float, frame_height: float) -> None:
        self.__view_instance.center = (frame_width * 0.5, frame_height * 0.5)
        self.__scale_factor = self.get_scale_factor(frame_height)
        self.__view_instance.transform = ui.Transform.scale(self.__scale_factor, self.__scale_factor)

    def adjust_layout_for_keyboard_height(self, padding_of_keyboard: float) -> None:
        scroll_menu_bottom = self.__view_instance.y + self.__view_instance["config_menu_scroll"].y +\
                             self.__view_instance["config_menu_scroll"].height
        if padding_of_keyboard < scroll_menu_bottom:
            extension_of_contents = (scroll_menu_bottom - padding_of_keyboard) * math.sqrt(self.__scale_factor)
        else:
            extension_of_contents = 0
        self.__view_instance["config_menu_scroll"].content_size = \
            self.__scroll_menu_handler.get_scroll_view_size(extension_of_contents)

    def set_button_action(self, save_config_action, set_default_action, cancel_configuration_action) -> None:
        self.__view_instance['save_config_button'].action = save_config_action
        self.__view_instance['set_default_button'].action = set_default_action
        self.__view_instance['cancel_configuration_button'].action = cancel_configuration_action

    def switch_view_enabled(self, will_enabled: bool) -> None:
        for subview in self.__view_instance.subviews:
            if hasattr(subview, 'enabled'):
                subview.enabled = will_enabled
        self.__scroll_menu_handler.switch_view_enabled(will_enabled)

    def enable_view(self) -> None:
        self.__view_instance.touch_enabled = True
        self.__view_instance["config_menu_scroll"].touch_enabled = True
        self.switch_view_enabled(True)
        self.__view_instance.alpha = 1.0

    def disable_view(self) -> None:
        self.__view_instance.touch_enabled = False
        self.__view_instance["config_menu_scroll"].touch_enabled = False
        self.switch_view_enabled(False)
        self.__view_instance.alpha = 0.2

    def get_configuration_inputs(self) -> AppSettingsInputs:
        return self.__scroll_menu_handler.get_all_setting_values()
