from custom_types.settings import MusicPlayerSettings


class MusicPlayerConfig:
    def __init__(self, focus_playlist_name: str, break_playlist_name: str, is_random_mode: bool) -> None:
        self.__focus_playlist_name = focus_playlist_name
        self.__break_playlist_name = break_playlist_name
        self.__is_random_mode = is_random_mode

    def get_settings(self) -> MusicPlayerSettings:
        return {"focus_playlist_name": self.__focus_playlist_name,
                "break_playlist_name": self.__break_playlist_name,
                "is_random_mode": self.__is_random_mode}
