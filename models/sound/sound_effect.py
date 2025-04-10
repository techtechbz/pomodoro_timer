from enum import Enum
from sound import play_effect
from time import sleep
from threading import Thread
from typing import Callable

from models.configuration.config_class.alarm_config import AlarmConfig


class AlarmName(Enum):
	デフォルト = 0
	ピアノ = 1
	西鉄 = 2
	
	@classmethod
	def get_alarm_list(cls):
		return list(map(lambda member: member.name, cls))


class TimerSoundEffect:
	def __init__(self, config: AlarmConfig) -> None:
		settings = config.get_settings()
		self.__alarm_index = settings['alarm_index']
		self.__notice_time = self.calculate_notice_time(settings)
		self.__thread = None

	def apply_renewal_config(self, config: AlarmConfig) -> None:
		updated_settings = config.get_settings()
		self.__alarm_index = updated_settings['alarm_index']
		self.__notice_time = self.calculate_notice_time(updated_settings)

	@staticmethod
	def calculate_notice_time(settings) -> tuple[int, int]:
		if settings['will_notice']:
			return settings['notice_seconds'] // 60, settings['notice_seconds'] % 60
		else:
			return -1, -1

	@staticmethod
	def play_default_alarm() -> None:
		play_effect('piano:D3')
		sleep(0.08)
		play_effect('piano:F3#')
		sleep(0.08)
		play_effect('piano:A3')

	@staticmethod
	def play_piano_alarm() -> None:
		play_effect('piano:D3')
		sleep(0.15)
		play_effect('piano:D4')
		sleep(0.15)
		play_effect('piano:A3')
		sleep(0.15)
		play_effect('piano:F4#')

	@staticmethod
	def play_nishitetsu_alarm() -> None:
		play_effect('piano:G3')
		sleep(0.01)
		play_effect('piano:B3', pitch=2)
		sleep(0.01)
		play_effect('piano:D4', pitch=2)
		sleep(0.01)
		play_effect('piano:G4', pitch=2)
		sleep(0.5)
		play_effect('piano:D4')
		sleep(0.25)
		play_effect('piano:G4')
		sleep(0.25)
		play_effect('piano:A3', pitch=2)
		sleep(0.25)
		play_effect('piano:D4', pitch=2)
		sleep(0.25)
		play_effect('piano:B3', pitch=2)
	
	def get_alarm(self) -> Callable[[], None]:
		alarm_name = AlarmName(self.__alarm_index)
		if alarm_name == AlarmName.デフォルト:
			return self.play_default_alarm
		elif alarm_name == AlarmName.ピアノ:
			return self.play_piano_alarm
		else:
			return self.play_nishitetsu_alarm

	def play_thread(self):
		self.__thread.start()
		del self.__thread
		self.__thread = None
	
	def play_alarm(self):
		if self.__thread is not None:
			print('thread is alive.')
			print(self.__thread)
			return
		self.__thread = Thread(target=self.get_alarm())
		self.play_thread()

	def play_notification(self):
		if self.__thread is not None:
			print('thread is alive.')
			print(self.__thread)
			return
		self.__thread = Thread(target=self.play_default_alarm)
		self.play_thread()

	def play_countdown(self) -> None:
		if self.__thread is not None:
			print('thread is alive.')
			print(self.__thread)
			return
		self.__thread = Thread(target=play_effect, args=('ui:switch27',))
		self.play_thread()

	def play_se(self, minute: int, second: int) -> None:
		if minute == 0 and second <= 3:
			self.play_countdown()
		if minute == self.__notice_time[0] and second == self.__notice_time[1]:
			self.play_notification()
