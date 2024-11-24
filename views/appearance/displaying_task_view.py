import ui


class DisplayingTaskViewManager:
    def __init__(self):
        self.__view_instance = ui.load_view("./pyui/appearance/displaying_task.pyui")

    def get_view_instance(self) -> ui.View:
        return self.__view_instance

    def set_edit_task_action(self, edit_task_action) -> None:
        self.__view_instance["edit_task_button"].action = edit_task_action

    def get_current_task_name(self) -> str:
        return self.__view_instance['task_name_label'].text

    def update_task_name_label(self, task_name: str) -> None:
        self.__view_instance["task_name_label"].text = task_name
