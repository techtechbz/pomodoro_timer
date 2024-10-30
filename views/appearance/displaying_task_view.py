import ui


class DisplayingTaskViewManager:
    def __init__(self):
        self.__view_instance = ui.load_view("./pyui/appearance/displaying_task.pyui")

    def get_view_instance(self):
        return self.__view_instance

    def set_edit_task_action(self, edit_task_action):
        self.__view_instance["edit_task_button"].action = edit_task_action

    def update_task_name_label(self, task_name):
        self.__view_instance["task_name_label"].text = task_name
