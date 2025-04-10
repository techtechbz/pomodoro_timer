from objc_util import ObjCClass, NSBundle
from threading import Thread
from typing import Optional

from models.configuration.config_class.music_player_config import MusicPlayerConfig


class MusicPlayer:
	def __init__(self, music_player_config: MusicPlayerConfig) -> None:
		self.__settings = music_player_config.get_settings()
		NSBundle.bundleWithPath_('/System/Library/Frameworks/MediaPlayer.framework').load()
		self.__player = ObjCClass('MPMusicPlayerController').systemMusicPlayer()
		self.__set_focus_playlist = False
		self.__focus_playlist = self.find_playlist(self.__settings["focus_playlist_name"])
		self.__break_playlist = self.find_playlist(self.__settings["break_playlist_name"])
		self.__thread: Optional[Thread] = None
		if self.__focus_playlist is not None:
			self.prepare_playlist(self.__focus_playlist)
			self.__set_focus_playlist = True
		else:
			self.prepare_playlist(self.__break_playlist)
	
	def apply_renewal_config(self, config: MusicPlayerConfig) -> None:
		updated_settings = config.get_settings()
		if updated_settings["focus_playlist_name"] != self.__settings["focus_playlist_name"]:
			self.__focus_playlist = self.find_playlist(updated_settings["focus_playlist_name"])
			if self.__set_focus_playlist:
				self.prepare_playlist(self.__focus_playlist)
		if updated_settings["break_playlist_name"] != self.__settings["break_playlist_name"]:
			self.__break_playlist = self.find_playlist(updated_settings["break_playlist_name"])
			if not self.__set_focus_playlist:
				self.prepare_playlist(self.__break_playlist)
		self.__settings = updated_settings
	
	@staticmethod
	def find_playlist(playlist_name: str):
		collections = ObjCClass('MPMediaQuery').playlistsQuery().collections()
		for playlist in collections:
			if str(playlist.valueForKey_("name")) == playlist_name:
				return playlist
		return None
	
	def prepare_playlist(self, playlist) -> None:
		if playlist is None:
			return
		self.__player.setQueueWithItemCollection(playlist)
		self.__player.prepareToPlay()
		self.shuffle_music()

	def is_not_set_playlist_on_mode(self, on_break: bool) -> bool:
		return (on_break and self.__break_playlist is None) or (not on_break and self.__focus_playlist is None)
	
	def shuffle_music(self) -> None:
		if self.__settings["is_random_mode"] and self.__player.shuffleMode() == 1:
			self.__player.shuffle()

	def start_music(self) -> None:
		self.__thread = Thread(target=self.__player.play)
		self.__thread.start()

	def restart_music(self, on_break: bool) -> None:
		# 切り替わったモード中に再生するプレイリストが設定されていない場合、再生しない。
		if self.is_not_set_playlist_on_mode(on_break):
			return
		self.shuffle_music()
		self.__player.play()
	
	def pause_music(self) -> None:
		self.__player.pause()

	def change_mode(self, on_break: bool) -> None:
		# プレイリストが同じ場合、再生(または無再生)を続ける
		if self.__settings["focus_playlist_name"] == self.__settings["break_playlist_name"]:
			return
		# 切り替わったモード中に再生するプレイリストが設定されていない場合、再生を止める。
		if self.is_not_set_playlist_on_mode(on_break):
			self.pause_music()
			return
		# 設定中のプレイリストが、これから切り替わるモードに合ったのもではないとき、プレイリストを再設定してから並行処理で再生する
		if on_break is self.__set_focus_playlist:
			self.stop_music()
			playlist = self.__break_playlist if on_break else self.__focus_playlist
			self.prepare_playlist(playlist)
			self.start_music()
			self.__set_focus_playlist = not on_break
		# 設定中のプレイリストが、これから切り替わるモードに合っているとき、並行処理を行わず再生する
		else:
			self.__player.play()

	def reset_thread(self) -> None:
		if self.__thread is not None:
			self.__thread.join()
			del self.__thread
			self.__thread = None

	def stop_music(self) -> None:
		self.__player.stop()
		self.reset_thread()
