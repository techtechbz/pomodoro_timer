from datetime import time

import pytest

from models.task_recorder.task_recorder import DateTimeFormatter


class TestDateTimeFormatter:
    @classmethod
    def setup_class(cls):
        cls.converter = DateTimeFormatter()

    @pytest.mark.parametrize('time_str,expected', [
        ('0:00:00', time(0, 0, 0)),
        ('23:59:59', time(23, 59, 59)),
        ('59:59', time(0, 59, 59)),
        ('59', time(0, 0, 59)),
        ('', time(0, 0, 0)),
        ('-', time(0, 0, 0)),
    ])
    def test_format_time_str_to_time(self, time_str, expected):
        assert self.converter.format_time_str_to_time(time_str) == expected

    @pytest.mark.parametrize('early_time,later_time,expected', [
        ('0:00:00', '0:00:01', 1),
        ('0:01:00', '0:01:01', 1),
        ('0:01:00', '0:02:00', 60),
        ('0:01:00', '0:02:01', 61),
        ('1:00:00', '2:00:00', 3600),
        ('1:00:00', '2:01:00', 3660),
        ('1:00:00', '2:01:01', 3661),
        ('1:59:00', '2:01:01', 121),
        ('0:00:00', '0:00:00', 0),
        ('23:59:59', '0:00:01', 2),
        ('23:59:59', '0:01:01', 62),
        ('23:59:59', '1:00:01', 3602),
        ('23:59:59', '1:01:01', 3662),
    ])
    def test_calculate_interval_seconds(self, early_time, later_time, expected):
        assert self.converter.calculate_interval_seconds(early_time, later_time) == expected

    @pytest.mark.parametrize('time_str,expected', [
        ('0:01', 1),
        ('1:01', 61),
        ('1:00:01', 3601),
        ('1:01:01', 3661),
    ])
    def test_format_time_str_to_seconds(self, time_str, expected):
        assert self.converter.format_time_str_to_seconds(time_str) == expected

    @pytest.mark.parametrize('sec,expected', [
        (1, '0:01'),
        (61, '1:01'),
        (3601, '1:00:01'),
        (3661, '1:01:01'),
    ])
    def test_format_seconds_to_time_str(self, sec, expected):
        assert self.converter.format_seconds_to_time_str(sec) == expected
