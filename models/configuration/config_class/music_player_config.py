class MusicPlayerConfig:
    def __init__(self, will_play_music, will_play_music_on_break, playlist_name, is_random_mode):
        self.__will_play_music = will_play_music
        self.__will_play_music_on_break = will_play_music_on_break
        self.__playlist_name = playlist_name
        self.__is_random_mode = is_random_mode

    def get_settings(self):
        return {"will_play_music": self.__will_play_music,
                "will_play_music_on_break": self.__will_play_music_on_break,
                "playlist_name": self.__playlist_name,
                "is_random_mode": self.__is_random_mode}
