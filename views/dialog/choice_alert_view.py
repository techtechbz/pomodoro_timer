import ui


class ChoiceAlertManager:
    def __init__(self):
        self.__view_instance = ui.load_view("./pyui/dialog/choice_alert.pyui")
        self.__ok_action = None
        self.__cancel_action = None

    def get_view_instance(self):
        return self.__view_instance

    def adjust_position(self, frame_width, frame_height):
        self.__view_instance.center = (frame_width * 0.5, frame_height * 0.5)

    def set_title(self, title):
        self.__view_instance["alert_title"].text = title

    def set_ok_action(self, ok_action):
        self.__view_instance['ok_button'].action = ok_action
        self.__ok_action = ok_action

    def set_cancel_action(self, cancel_action):
        self.__view_instance['cancel_button'].action = cancel_action
        self.__cancel_action = cancel_action

    def execute_ok_action(self):
        self.__ok_action()

    def execute_cancel_action(self):
        self.__cancel_action()

    def reset_action(self):
        del self.__ok_action
        del self.__cancel_action
        self.__ok_action = None
        self.__cancel_action = None
