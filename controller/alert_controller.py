import console
import ui

from views.dialog.choice_alert_view import ChoiceAlertManager


class AlertController:
    def __init__(self, frame_width: int, frame_height: int, add_subview, remove_subview) -> None:
        self.__choice_alert_manager = ChoiceAlertManager()
        self.adjust_position(frame_width, frame_height)
        self.add_subview = add_subview
        self.remove_subview = remove_subview
        self.__is_displayed_alert = False

    def execute_command(self, sender) -> None:
        if sender['title'] == 'confirm':
            self.__choice_alert_manager.execute_ok_action()
        if sender['title'] == 'interrupt':
            self.__choice_alert_manager.execute_cancel_action()

    def is_displayed_alert(self) -> bool:
        return self.__is_displayed_alert

    def adjust_position(self, frame_width, frame_height) -> None:
        self.__choice_alert_manager.adjust_position(frame_width, frame_height)

    @ui.in_background
    def show_message_alert(self, text: str) -> None:
        console.alert(text, button1="OK", hide_cancel_button=True)

    def show_choice_alert(self, title: str, ok_action, cancel_action=None) -> None:
        self.__is_displayed_alert = True
        self.__choice_alert_manager.set_title(title)
        self.__choice_alert_manager.set_ok_action(ok_action)

        def close_alert(_=None) -> None:
            if cancel_action is not None:
                cancel_action()
            self.close_choice_alert()

        self.__choice_alert_manager.set_cancel_action(close_alert)
        self.add_subview(self.__choice_alert_manager.get_view_instance())

    def close_choice_alert(self) -> None:
        self.__is_displayed_alert = False
        self.__choice_alert_manager.reset_action()
        self.remove_subview(self.__choice_alert_manager.get_view_instance())
