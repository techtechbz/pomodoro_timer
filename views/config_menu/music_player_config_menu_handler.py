from objc_util import ObjCClass
from typing import Final, Optional
import ui

from custom_types.appearance import ColorCode
from custom_types.settings import MusicPlayerSettings


class DirectToMusicAppViewHandler:
    def __init__(self, scroll_view_width: float, frame_height: float):
        self.__view_instance = ui.load_view("./pyui/config_menu/direct_to_music_app_sentence.pyui")
        self.sizing(scroll_view_width, frame_height)

    def get_scale_factor(self, frame_width: float) -> float:
        return frame_width / self.__view_instance.width

    def sizing(self, frame_width: float, frame_height: float) -> None:
        scale_factor = self.get_scale_factor(frame_width)
        self.__view_instance.transform = ui.Transform.scale(scale_factor, scale_factor)
        self.__view_instance.center = (frame_width * 0.5, frame_height * 0.5)

    def get_view_instance(self) -> ui.View:
        return self.__view_instance


class PlaylistConfigItemHandler:
    def __init__(self, playlist_name: str, item_name: str) -> None:
        self.__playlist_config_item_view = ui.load_view("./pyui/config_menu/playlist_config_item.pyui")
        self.__playlist_config_item_view["playlist_name_label"].text = playlist_name
        self.__playlist_config_item_view.name = item_name
        self.__playlist_config_item_view.border_color = ColorCode("#ffffff")
        self.__playlist_config_item_view.border_width = 1

    def get_view_instance(self) -> ui.View:
        return self.__playlist_config_item_view

    def set_select_button_action(self, action) -> None:
        self.__playlist_config_item_view["select_button"].action = action

    def style_appearance(self, height: float, y: float, default_tint_color: ColorCode,
                         background_color: ColorCode) -> ui.View:
        self.__playlist_config_item_view.height = height
        self.__playlist_config_item_view.y = y
        self.__playlist_config_item_view["select_button"].tint_color = default_tint_color
        self.__playlist_config_item_view.background_color = background_color


class PlaylistConfigRadioGroupAppearanceSettings:
    def __init__(self) -> None:
        self.__item_height: Final[int] = 40
        self.__even_item_background_color: Final[ColorCode] = ColorCode("#cccccc")
        self.__odd_item_background_color: Final[ColorCode] = ColorCode("#eeeeee")
        self.__selected_button_tint_color: Final[ColorCode] = ColorCode("#4f8aff")
        self.__unselected_button_tint_color: Final[ColorCode] = ColorCode("#bbbbbb")

    def return_item_height(self) -> int:
        return self.__item_height

    def calculate_scroll_contents_height(self, item_number: int) -> int:
        return self.__item_height * item_number

    def calculate_item_position_vertical_axis(self, order: int) -> int:
        return self.__item_height * order

    def distinguish_select_button_tint_color(self, is_selected: bool) -> ColorCode:
        if is_selected:
            return self.__selected_button_tint_color
        else:
            return self.__unselected_button_tint_color

    def distinguish_item_background_color(self, order: int) -> ColorCode:
        if order % 2 == 0:
            return self.__even_item_background_color
        else:
            return self.__odd_item_background_color


class PlaylistConfigRadioGroupHandler:
    def __init__(self, scroll_view: ui.View, saved_playlist_name: str) -> None:
        self.__appearance_setting = PlaylistConfigRadioGroupAppearanceSettings()
        self.__scroll_view = scroll_view
        self.__scroll_view.border_color = ColorCode("#000000")
        self.__scroll_view.border_width = 1
        self.__available_playlist = self.get_available_playlist()
        self.__selected_playlist_name = self.choice_playlist_name(saved_playlist_name)

    def get_selected_playlist_name(self) -> str:
        return self.__selected_playlist_name

    def choice_playlist_name(self, saved_playlist_name: str) -> str:
        if saved_playlist_name in self.__available_playlist.keys():
            return saved_playlist_name
        return ""

    @staticmethod
    def get_playlist_config_item_name(order: int) -> str:
        return f"playlist_{order}"

    def get_available_playlist(self) -> dict[str, str]:
        collections = ObjCClass('MPMediaQuery').playlistsQuery().collections()
        return {str(playlist.valueForKey_("name")): self.get_playlist_config_item_name(i)
                for i, playlist in enumerate(collections)}

    def insert_scroll_view_contents(self) -> None:
        if self.__available_playlist == {}:
            self.insert_direct_to_music_app_sentence_view()
        else:
            self.setting_appearance_of_group_ratio()
            self.insert_playlist_config_item()

    def setting_appearance_of_group_ratio(self) -> None:
        content_height = self.__appearance_setting.calculate_scroll_contents_height(len(self.__available_playlist))
        self.__scroll_view.content_size = self.__scroll_view.width, content_height

    def insert_direct_to_music_app_sentence_view(self) -> None:
        direct_to_music_app_sentence_view = \
            DirectToMusicAppViewHandler(self.__scroll_view.width, self.__scroll_view.height).get_view_instance()
        self.__scroll_view.add_subview(direct_to_music_app_sentence_view)

    def insert_playlist_config_item(self) -> None:
        for i, playlist_info in enumerate(self.__available_playlist.items()):
            playlist_name, item_name = playlist_info
            playlist_config_item_handler = PlaylistConfigItemHandler(playlist_name, item_name)
            height = self.__appearance_setting.return_item_height()
            y = self.__appearance_setting.calculate_item_position_vertical_axis(i)
            default_tint_color = self.__appearance_setting.distinguish_select_button_tint_color(
                playlist_name == self.__selected_playlist_name)
            background_color = self.__appearance_setting.distinguish_item_background_color(i)
            playlist_config_item_handler.style_appearance(height, y, default_tint_color, background_color)
            playlist_config_item_handler.set_select_button_action(self.switch_selected_playlist_name)
            self.__scroll_view.add_subview(playlist_config_item_handler.get_view_instance())

    def unselect_current_playlist(self) -> None:
        if self.__selected_playlist_name != "":
            previous_selected_button = \
                self.__scroll_view[self.__available_playlist[self.__selected_playlist_name]]["select_button"]
            previous_selected_button.tint_color = self.__appearance_setting.distinguish_select_button_tint_color(False)

    def set_selected_playlist_name(self, updated_playlist_name: str) -> None:
        self.unselect_current_playlist()
        if updated_playlist_name != "":
            applicable_button = self.__scroll_view[self.__available_playlist[updated_playlist_name]]["select_button"]
            applicable_button.tint_color = self.__appearance_setting.distinguish_select_button_tint_color(True)
            self.__selected_playlist_name = updated_playlist_name

    def switch_selected_playlist_name(self, sender: ui.View) -> None:
        self.unselect_current_playlist()
        if self.__selected_playlist_name == sender.superview["playlist_name_label"].text:
            self.__selected_playlist_name = ""
            return
        self.__selected_playlist_name = sender.superview["playlist_name_label"].text
        sender.tint_color = self.__appearance_setting.distinguish_select_button_tint_color(True)


class MusicPlayerConfigMenuHandler:
    def __init__(self) -> None:
        self.__view_instance = ui.load_view("./pyui/config_menu/music_player_config_menu.pyui")
        self.__current_music_player_settings: Optional[ui.View] = None
        self.__playlist_config_group_ratio_handler = PlaylistConfigRadioGroupHandler(
            self.__view_instance["select_playlist_scroll_view"],
            ""
        )
        self.__playlist_config_group_ratio_handler.insert_scroll_view_contents()

    def get_view_instance(self) -> ui.View:
        return self.__view_instance

    def reset_settings(self, music_player_settings: MusicPlayerSettings) -> None:
        self.__current_music_player_settings = music_player_settings
        self.insert_field_text()

    def write_out_field_inputs(self) -> None:
        self.__current_music_player_settings["will_play_music"] = self.__view_instance["will_play_music_switch"].value
        self.__current_music_player_settings["will_play_music_on_break"] = \
            self.__view_instance["will_play_music_on_break_switch"].value
        self.__current_music_player_settings["playlist_name"] = \
            self.__playlist_config_group_ratio_handler.get_selected_playlist_name()
        self.__current_music_player_settings["is_random_mode"] = self.__view_instance["is_random_mode_switch"].value

    def insert_field_text(self) -> None:
        self.__view_instance["will_play_music_switch"].value = self.__current_music_player_settings["will_play_music"]
        self.__view_instance["will_play_music_on_break_switch"].value = \
            self.__current_music_player_settings["will_play_music_on_break"]
        self.__playlist_config_group_ratio_handler.set_selected_playlist_name(
            self.__current_music_player_settings["playlist_name"]
        )
        self.__view_instance["is_random_mode_switch"].value = self.__current_music_player_settings["is_random_mode"]

    def get_setting_values(self) -> MusicPlayerSettings:
        return self.__current_music_player_settings

    @staticmethod
    def switch_subview_enabled(subview: ui.View, will_enabled: bool) -> None:
        if hasattr(subview, 'enabled'):
            subview.enabled = will_enabled
        if hasattr(subview, 'touch_enabled'):
            subview.touch_enabled = will_enabled

    def switch_enabled(self, will_enabled: bool) -> None:
        scroll_view = self.__view_instance['select_playlist_scroll_view']
        for subview in scroll_view.subviews:
            if hasattr(subview, "subviews"):
                for s in subview.subviews:
                    self.switch_subview_enabled(s, will_enabled)
            self.switch_subview_enabled(subview, will_enabled)
