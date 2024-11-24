from objc_util import ObjCClass, NSBundle
import random

from models.configuration.config_class.music_player_config import MusicPlayerConfig


class MusicPlayer:
	def __init__(self, music_player_config: MusicPlayerConfig) -> None:
		self.__settings = music_player_config.get_settings()
		NSBundle.bundleWithPath_('/System/Library/Frameworks/MediaPlayer.framework').load()
		self.__player = ObjCClass('MPMusicPlayerController').systemMusicPlayer()
		if self.__settings["playlist_name"] != "":
			self.prepare_playlist(self.__settings["playlist_name"])
	
	def apply_renewal_config(self, config: MusicPlayerConfig) -> None:
		updated_settings = config.get_settings()
		if updated_settings["playlist_name"] != self.__settings["playlist_name"]:
			self.prepare_playlist(updated_settings["playlist_name"])
		if updated_settings != self.__settings:
			self.__settings = updated_settings
	
	@staticmethod
	def get_playlist(playlist_name: str):
		collections = ObjCClass('MPMediaQuery').playlistsQuery().collections()
		for playlist in collections:
			if str(playlist.valueForKey_("name")) == playlist_name:
				return playlist
	
	def prepare_playlist(self, playlist_name: str) -> None:
		playlist = self.get_playlist(playlist_name)
		self.__player.setQueueWithItemCollection(playlist)
		self.__player.prepareToPlay()
		if self.__settings["is_random_mode"]:
			self.skip_several_music()
	
	def skip_several_music(self) -> None:
		for i in range(0, random.randint(1, 20)):
			self.__player.skipToNextItem()
	
	def start_music(self) -> None:
		if self.__settings["is_random_mode"]:
			self.skip_several_music()
		self.__player.play()

	def restart_music(self, on_break: bool) -> None:
		if (on_break and self.__settings["will_play_music_on_break"]) or \
				(not on_break and self.__settings["will_play_music"]):
			return
		self.__player.play()
	
	def pause_music(self) -> None:
		self.__player.pause()

	def stop_music(self) -> None:
		self.__player.stop()

	def change_to_focus_mode(self) -> None:
		if self.__settings["will_play_music"]:
			self.start_music()
		else:
			self.pause_music()
	
	def change_to_break_mode(self) -> None:
		if self.__settings["will_play_music_on_break"]:
			self.start_music()
		else:
			self.pause_music()
