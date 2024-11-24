from typing import TypedDict


PresetSettings = TypedDict('PresetSettings', {'preset_index': int})

TimerSettings = TypedDict('TimerSettings', {
    "preset_name": str,
    "task_minutes": int,
    "short_break_minutes": int,
    "long_break_minutes": int,
    "loop_times": int,
    "will_count": bool,
    "count_seconds": int
})

TimerInputs = TypedDict('TimerInputs', {
    "preset_name": str,
    "task_minutes": str,
    "short_break_minutes": str,
    "long_break_minutes": str,
    "loop_times": str,
    "will_count": bool,
    "count_seconds": str
})

TimerSettingsList = list[TimerSettings]

TimerInputsList = list[TimerInputs]

AlarmSettings = TypedDict('AlarmSettings', {'alarm_index': int})

TaskRecorderSettings = TypedDict('TaskRecorderSettings', {
    "will_record_task": bool,
    "will_record_break": bool,
    "file_format_index": int,
    "save_file_path": str
})

MusicPlayerSettings = TypedDict('MusicPlayerSettings', {
    "will_play_music": bool,
    "will_play_music_on_break": bool,
    "playlist_name": str,
    "is_random_mode": bool
})

AppSettings = TypedDict('AppSettings', {
    "preset_index_settings": PresetSettings,
    "timer_settings_list": TimerSettingsList,
    "task_recorder_settings": TaskRecorderSettings,
    "alarm_settings": AlarmSettings,
    "music_player_settings": MusicPlayerSettings
})

AppSettingsInputs = TypedDict('AppSettingsInputs', {
    "preset_index_settings": PresetSettings,
    "timer_settings_list": TimerInputsList,
    "task_recorder_settings": TaskRecorderSettings,
    "alarm_settings": AlarmSettings,
    "music_player_settings": MusicPlayerSettings
})
