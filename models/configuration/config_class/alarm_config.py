class AlarmConfig:
	def __init__(self, alarm_index):
		self.__alarm_index = alarm_index
		
	def get_settings(self):
		return {"alarm_index": self.__alarm_index}
