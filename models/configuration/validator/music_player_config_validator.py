from objc_util import ObjCClass

from models.configuration.validator.validation_status import ValidationStatus


class MusicPlayerConfigValidator:
    def __init__(self):
        self.__status: ValidationStatus = ValidationStatus.unverified
        self.__message: str = ""

    def validation(self, focus_playlist_name: str, break_playlist_name: str, is_random_mode: bool):
        self.__status = ValidationStatus.unverified
        self.__message = ""
        if self.__status == ValidationStatus.unverified:
            self.__status = ValidationStatus.success

        return {"focus_playlist_name": focus_playlist_name,
                "break_playlist_name": break_playlist_name,
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
