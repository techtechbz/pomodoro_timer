from enum import Enum
from sound import play_effect
from time import sleep
from threading import Thread


class AlarmName(Enum):
	デフォルト = 0
	ピアノ = 1
	
	@classmethod
	def get_alarm_list(cls):
		return list(map(lambda member: member.name, cls))


class TimerSoundEffect:
	def __init__(self, config):
		self.__thread = None
		self.__settings = config.get_settings()
		self.__countdown_se_tag = 'ui:switch27'
	
	def apply_renewal_config(self, config):
		updated_settings = config.get_settings()
		if self.__settings == updated_settings:
			self.__settings = updated_settings
	
	def countdown_sound(self):
		if self.__thread is None:
			self.__thread = Thread(target=play_effect, args=(self.__countdown_se_tag,))
			self.__thread.start()
			del self.__thread
			self.__thread = None
	
	@staticmethod
	def play_default_alarm():
		play_effect('piano:D3')
		sleep(0.15)
		play_effect('piano:D4')
		sleep(0.15)
		play_effect('piano:A3')
		sleep(0.15)
		play_effect('piano:F4#')
	
	@staticmethod
	def play_piano_alarm():
		play_effect('piano:D3')
		sleep(0.15)
		play_effect('piano:D4')
		sleep(0.15)
		play_effect('piano:A3')
		sleep(0.15)
		play_effect('piano:F4#')
	
	def get_alarm(self):
		alarm_name = AlarmName(self.__settings["alarm_index"])
		if alarm_name == AlarmName.デフォルト:
			return self.play_default_alarm
		else:
			return self.play_piano_alarm
	
	def play_alarm(self):
		if self.__thread is None:
			self.__thread = Thread(target=self.get_alarm())
			self.__thread.start()
			del self.__thread
			self.__thread = None

