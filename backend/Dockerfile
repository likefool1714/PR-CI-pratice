# 1) 베이스 이미지: 파이썬이 설치된 가벼운 리눅스
FROM python:3.12-slim

# 2) 컨테이너 안 작업 폴더
WORKDIR /srv

# 3) 의존성 먼저 설치 (코드만 바뀌면 이 단계는 캐시를 재사용해서 빌드가 빨라짐)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4) 앱 코드 복사
COPY app ./app

# 5) 컨테이너가 쓰는 포트 안내 (문서 역할)
EXPOSE 8000

# 6) 컨테이너가 시작될 때 실행할 명령
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
