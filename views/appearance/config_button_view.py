import ui


class ConfigButtonViewManager:
    def __init__(self) -> None:
        self.__view_instance = ui.load_view("./pyui/appearance/config_button.pyui")

    def get_view_instance(self) -> ui.View:
        return self.__view_instance

    def set_button_action(self, launch_music_app_action, config_action) -> None:
        self.__view_instance["launch_music_app_button"].action = launch_music_app_action
        self.__view_instance["config_button"].action = config_action
