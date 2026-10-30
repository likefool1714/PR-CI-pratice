"""발표 분석에 쓰일 작은 계산 로직 (단위 테스트 연습용)."""


def words_per_minute(word_count: int, seconds: float) -> float:
    """발화 속도: 1분당 단어 수를 계산합니다."""
    if seconds <= 0:
        raise ValueError("seconds는 0보다 커야 합니다")
    return round(word_count / seconds * 60, 1)
