from objc_util import ObjCClass

from models.configuration.validator.validation_status import ValidationStatus


class MusicPlayerConfigValidator:
    def __init__(self):
        self.__status: ValidationStatus = ValidationStatus.unverified
        self.__message: str = ""

    def validation(self, will_play_music: bool, will_play_music_on_break: bool, playlist_name: str,
                   is_random_mode: bool):
        self.__status = ValidationStatus.unverified
        self.__message = ""
        if will_play_music or will_play_music_on_break:
            if playlist_name != "":
                playlist = self.get_playlist(playlist_name)
                if playlist is None:
                    self.__message = "・プレイリスト: プレイリストが見つかりませんでした。"
                    self.__status = ValidationStatus.error
            else:
                self.__message = "・プレイリスト: プレイリストが指定されていません。"
                self.__status = ValidationStatus.error

        if self.__status == ValidationStatus.unverified:
            self.__status = ValidationStatus.success

        return {"will_play_music": will_play_music,
                "will_play_music_on_break": will_play_music_on_break,
                "playlist_name": playlist_name,
                "is_random_mode": is_random_mode}

    @staticmethod
    def get_playlist(playlist_name: str):
        collections = ObjCClass('MPMediaQuery').playlistsQuery().collections()
        for playlist in collections:
            if str(playlist.valueForKey_("name")) == playlist_name:
                return playlist
        return None

    def return_validation_result(self):
        return self.__status, self.__message

    def is_valid_settings(self) -> bool:
        return self.__status == ValidationStatus.success
