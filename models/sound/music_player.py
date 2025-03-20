from objc_util import ObjCClass, NSBundle
import random

from models.configuration.config_class.music_player_config import MusicPlayerConfig


class MusicPlayer:
	def __init__(self, music_player_config: MusicPlayerConfig) -> None:
		self.__settings = music_player_config.get_settings()
		NSBundle.bundleWithPath_('/System/Library/Frameworks/MediaPlayer.framework').load()
		self.__player = ObjCClass('MPMusicPlayerController').systemMusicPlayer()
		self.__max_skip_times = 0
		self.__focus_playlist = None
		self.__break_playlist = None
		self.get_playlists()
		self.__set_focus_playlist = False

	def apply_renewal_config(self, config: MusicPlayerConfig) -> None:
		updated_settings = config.get_settings()
		if updated_settings != self.__settings:
			self.__settings = updated_settings
			self.get_playlists()
	
	@staticmethod
	def find_playlist(playlist_name: str):
		collections = ObjCClass('MPMediaQuery').playlistsQuery().collections()
		for playlist in collections:
			if str(playlist.valueForKey_("name")) == playlist_name:
				return playlist
		return None
	
	def prepare_playlist(self, playlist) -> None:
		music_num = len(playlist.items())
		max_skip_num = 30
		self.__max_skip_times = music_num if music_num <= max_skip_num else max_skip_num
		self.__player.setQueueWithItemCollection(playlist)
		self.__player.prepareToPlay()

	def get_playlists(self):
		self.__focus_playlist = self.find_playlist(self.__settings["focus_playlist_name"])
		self.__break_playlist = self.find_playlist(self.__settings["break_playlist_name"])
		if self.is_found_focus_playlist():
			self.prepare_playlist(self.__focus_playlist)
			self.__set_focus_playlist = True
		elif self.is_found_break_playlist():
			self.prepare_playlist(self.__break_playlist)
	
	def is_found_focus_playlist(self) -> bool:
		return self.__focus_playlist is not None
	
	def is_found_break_playlist(self) -> bool:
		return self.__break_playlist is not None

	def set_playlist_on_mode(self, on_break: bool) -> bool:
		return (on_break and not self.is_found_break_playlist()) or (not on_break and not self.is_found_focus_playlist())
	
	def skip_several_music(self) -> None:
		for i in range(0, random.randint(1, self.__max_skip_times)):
			self.__player.skipToNextItem()

	def start_music(self) -> None:
		if self.__settings["is_random_mode"]:
			self.skip_several_music()
		self.__player.play()

	def restart_music(self, on_break: bool) -> None:
		if self.set_playlist_on_mode(on_break):
			return
		self.__player.play()
	
	def pause_music(self) -> None:
		self.__player.pause()

	def change_mode(self, on_break: bool) -> None:
		# プレイリストが同じ場合、再生(または無再生)を続ける
		if self.__settings["focus_playlist_name"] == self.__settings["break_playlist_name"]:
			return
		# 切り替わったモード中に再生するプレイリストが設定されていない場合、再生を止める。
		if self.set_playlist_on_mode(on_break):
			self.pause_music()
			return
		# 切り替わったモードと、設定中のプレイリストのモードが異なる場合、プレイリストを再設定する
		if on_break is self.__set_focus_playlist:
			playlist = self.__break_playlist if on_break else self.__focus_playlist
			self.prepare_playlist(playlist)
			self.__set_focus_playlist = not on_break
		# 音楽を再生する
		self.start_music()

	def stop_music(self) -> None:
		self.__player.stop()
