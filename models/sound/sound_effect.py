from enum import Enum
from sound import play_effect
from time import sleep
from threading import Thread
from typing import Callable

from models.configuration.config_class.alarm_config import AlarmConfig


class AlarmName(Enum):
	デフォルト = 0
	ピアノ = 1
	
	@classmethod
	def get_alarm_list(cls):
		return list(map(lambda member: member.name, cls))


class AlarmPlayer:
	def __init__(self, alarm_index: int):
		self.__alarm_index = alarm_index
		self.__thread = None

	@staticmethod
	def play_default_alarm() -> None:
		play_effect('piano:D3')
		sleep(0.08)
		play_effect('piano:F3#')

	@staticmethod
	def play_piano_alarm() -> None:
		play_effect('piano:D3')
		sleep(0.15)
		play_effect('piano:D4')
		sleep(0.15)
		play_effect('piano:A3')
		sleep(0.15)
		play_effect('piano:F4#')

	def get_alarm(self) -> Callable[[], None]:
		alarm_name = AlarmName(self.__alarm_index)
		if alarm_name == AlarmName.デフォルト:
			return self.play_default_alarm
		else:
			return self.play_piano_alarm

	def define_playing_thread(self):
		self.__thread = Thread(target=self.get_alarm())
	
	def set_alarm(self, alarm_index: int) -> None:
		self.__alarm_index = alarm_index
		self.define_playing_thread()

	def play(self) -> None:
		self.__thread.start()
		del self.__thread
		self.define_playing_thread()


class CountDownPlayer:
	def __init__(self):
		self.__countdown_se_tag = 'ui:switch27'
		self.__thread = None
		self.define_playing_thread()

	def define_playing_thread(self):
		self.__thread = Thread(target=play_effect, args=(self.__countdown_se_tag,))
	
	def play(self) -> None:
		self.__thread.start()
		del self.__thread
		self.define_playing_thread()


class TimerSoundEffect:
	def __init__(self, config: AlarmConfig) -> None:
		self.__settings = config.get_settings()
		self.__alarm_player = AlarmPlayer(self.__settings['alarm_index'])
		self.__countdown_player = CountDownPlayer()

	def apply_renewal_config(self, config: AlarmConfig) -> None:
		updated_settings = config.get_settings()
		if self.__settings != updated_settings:
			self.__settings = updated_settings
			self.__alarm_player.set_alarm(self.__settings['alarm_index'])

	def play_alarm(self):
		self.__alarm_player.play()
	
	def play_se(self, minutes: int, seconds: int) -> None:
		if minutes >= 1:
			return
		if seconds <= 3:
			self.__countdown_player.play()

