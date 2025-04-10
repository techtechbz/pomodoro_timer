from objc_util import nsurl, UIApplication
from typing import Callable, Final, Optional
import ui

from controller.alert_controller import AlertController
from custom_types.command import Command
from models.configuration.config_provider import AppConfig, ConfigProvider
from views.appearance.config_button_view import ConfigButtonViewManager
from views.dialog.config_dialog_view import ConfigDialogViewManager


class ConfigurationController:
    def __init__(self, alert_controller: AlertController,
                 get_open_dialog_method: Callable[[ui.View], Callable[[], None]],
                 get_close_dialog_method: Callable[[ui.View], Callable[[], None]],
                 apply_renewal_config: Callable[[AppConfig, str], None]) -> None:
        # 設定項目を取得する
        self.__alert_controller: Final[AlertController] = alert_controller
        self.apply_renewal_config = apply_renewal_config
        self.__config_provider: Final[ConfigProvider] = ConfigProvider()
        self.__config: Optional[AppConfig] = self.__config_provider.get_saved_config()
        self.__config_dialog_view_manager: Final[ConfigDialogViewManager] = ConfigDialogViewManager()
        self.__config_dialog_view_manager.set_button_action(self.show_checking_to_save_config_alert,
                                                            self.show_checking_to_set_default_alert,
                                                            self.show_checking_to_cancel_alert)
        self.open_dialog = get_open_dialog_method(self.__config_dialog_view_manager.get_view_instance())
        self.close_dialog = get_close_dialog_method(self.__config_dialog_view_manager.get_view_instance())
        self.__config_button_view_manager: Final[ConfigButtonViewManager] = ConfigButtonViewManager()
        self.__config_button_view_manager.set_button_action(self.launch_music_app, self.open_config_dialog)
        self.__is_displaying_dialog = False

    def sizing(self, frame_width: float, frame_height: float) -> None:
        self.__config_dialog_view_manager.sizing(frame_width, frame_height)

    def adjust_layout_for_keyboard_height(self, keyboard_height: float) -> None:
        self.__config_dialog_view_manager.adjust_layout_for_keyboard_height(keyboard_height)

    def get_saved_config(self) -> Optional[AppConfig]:
        return self.__config

    def get_preset_name(self) -> str:
        return self.__config.get_preset_name()

    def get_config_button_view_instance(self) -> ui.View:
        return self.__config_button_view_manager.get_view_instance()

    def is_displaying_dialog(self) -> bool:
        return self.__is_displaying_dialog

    def open_config_dialog(self, _=None) -> None:
        self.__config_dialog_view_manager.apply_current_config(self.__config)
        self.open_dialog()
        self.__is_displaying_dialog = True

    def close_config_dialog(self) -> None:
        self.close_dialog()
        self.__is_displaying_dialog = False
        self.__config_dialog_view_manager.enable_view()

    def execute_command(self, sender: Command) -> None:
        if sender['title'] == 'music':
            self.launch_music_app()
        if sender['title'] == 'config':
            self.open_config_dialog()

        if self.__alert_controller.is_displayed_alert():
            self.__alert_controller.execute_command(sender)
            return
        if sender['title'] == 'save':
            self.show_checking_to_save_config_alert()
        elif sender['title'] == 'default':
            self.show_checking_to_set_default_alert()
        elif sender['title'] == 'interrupt':
            self.show_checking_to_cancel_alert()

    def get_validation_error_message(self) -> str:
        return f"現在の設定では、タイマーを正常に起動できません。\n設定画面より再設定を行なってください。" \
               f"\n\n{self.__config_provider.get_alert_message()}"

    def change_timer_preset(self, preset_index: int) -> None:
        self.__config.set_preset_index(preset_index)
        self.__config_provider.replace_config(self.__config)

    @staticmethod
    def launch_music_app(_=None) -> None:
        UIApplication.sharedApplication()._openURL_(nsurl("https://music.apple.com/jp"))

    def show_checking_to_save_config_alert(self, _=None) -> None:
        self.__config_dialog_view_manager.disable_view()
        self.__alert_controller.show_choice_alert("設定を保存しますか?", self.save_config, self.cancel)

    def show_checking_to_set_default_alert(self, _=None) -> None:
        self.__config_dialog_view_manager.disable_view()
        self.__alert_controller.show_choice_alert("設定値をデフォルトに戻しますか?", self.set_default)

    def show_checking_to_cancel_alert(self, _=None) -> None:
        self.__config_dialog_view_manager.disable_view()
        self.__alert_controller.show_choice_alert("設定を変更せずに終了しますか?",
                                                  self.interrupt_configuration, self.cancel)

    def cancel(self, _=None) -> None:
        self.__alert_controller.close_choice_alert()
        self.__config_dialog_view_manager.enable_view()

    def save_config(self, _=None) -> None:
        self.__alert_controller.close_choice_alert()
        inputs = self.__config_dialog_view_manager.get_configuration_inputs()
        replaced_config = self.__config_provider.save_input_settings(inputs)
        alert_message = self.__config_provider.get_alert_message()
        if replaced_config is None:
            self.__alert_controller.show_message_alert(alert_message)
            self.__config_dialog_view_manager.enable_view()
            return
        self.close_config_dialog()
        self.__config = replaced_config
        self.apply_renewal_config(replaced_config, alert_message)

    def set_default(self, _=None) -> None:
        self.__config_dialog_view_manager.set_default_settings_inputs()
        self.cancel()
        self.__alert_controller.show_message_alert("設定をデフォルトに戻しました!")

    def interrupt_configuration(self, _=None) -> None:
        self.__alert_controller.close_choice_alert()
        self.close_config_dialog()
