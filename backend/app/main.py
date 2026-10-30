from fastapi import FastAPI

from app.speech import words_per_minute

app = FastAPI(title="actions-practice backend")


@app.get("/health")
def health():
    # 서버가 살아 있는지 확인하는 API (CI의 실행 검증에서 호출)
    return {"status": "ok"}


@app.get("/speech-rate")
def speech_rate(words: int, seconds: float):
    # 예: /speech-rate?words=150&seconds=60  ->  {"wpm": 150.0}
    return {"wpm": words_per_minute(words, seconds)}
