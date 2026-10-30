import pytest

from app.speech import words_per_minute


def test_150_words_in_60_seconds():
    assert words_per_minute(150, 60) == 150.0


def test_half_minute():
    assert words_per_minute(60, 30) == 120.0


def test_zero_seconds_is_error():
    with pytest.raises(ValueError):
        words_per_minute(10, 0)
