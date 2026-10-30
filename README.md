# actions-practice

PR · Squash · GitHub Actions(CI) 연습용 저장소입니다. 팀 저장소와 분리된 **개인 public 저장소**에서 마음껏 성공과 실패를 만들어 보는 것이 목적입니다.

## 구조

```text
actions-practice/
├── .github/workflows/
│   ├── backend-ci.yml     # backend 폴더가 바뀐 PR → 테스트 + 이미지 빌드 + 실행 확인
│   └── frontend-ci.yml    # frontend 폴더가 바뀐 PR → 이미지 빌드 + 페이지 응답 확인
├── backend/               # FastAPI (발화 속도 계산 API)
│   ├── app/
│   │   ├── main.py        # /health, /speech-rate API
│   │   └── speech.py      # 발화 속도 계산 함수
│   ├── tests/             # 단위 테스트, API 테스트
│   ├── Dockerfile
│   ├── requirements.txt       # 실행에 필요한 패키지
│   ├── requirements-dev.txt   # 테스트용 패키지 추가
│   └── pytest.ini
├── frontend/              # nginx로 제공하는 정적 HTML
│   ├── index.html
│   └── Dockerfile
└── compose.yaml           # 내 맥에서 두 서비스를 한 번에 실행
```

## CI가 하는 일

```text
backend 변경 PR:  [test] pytest 실행 ──성공하면──▶ [docker] 이미지 빌드 → 컨테이너 실행 → /health 응답 확인
frontend 변경 PR: [docker] 이미지 빌드 → 컨테이너 실행 → 페이지에 "발표 코칭" 문구 확인
```

---

## 0. 준비 (처음 한 번)

1. GitHub에서 **New repository** → 이름 `actions-practice` → **Public** → README·.gitignore 추가 **체크하지 않기** → Create.
2. 맥 터미널에서 이 폴더로 이동 후:

```bash
git init                                  # 이 폴더를 Git 저장소로 만듦
git add .                                 # 모든 파일을 다음 커밋 대상으로 준비
git commit -m "init: 연습 저장소 구성"      # 첫 커밋
git branch -M main                        # 현재 브랜치 이름을 main으로
git remote add origin https://github.com/<내아이디>/actions-practice.git   # 원격 주소 등록
git push -u origin main                   # main을 GitHub에 올림 (-u: 추적 관계 설정)

git switch -c develop                     # main에서 develop 브랜치 생성 후 이동
git push -u origin develop                # develop도 GitHub에 올림
```

3. GitHub 저장소 **Settings → General**
   - Default branch: `develop` 으로 변경 (팀 규칙과 동일하게)
   - Pull Requests 항목: **Allow merge commits** ✅, **Allow squash merging** ✅
   - (선택) **Automatically delete head branches** ✅ → 머지 후 작업 브랜치 자동 삭제

---

## 미션 1. 성공하는 PR 한 바퀴

```bash
git switch develop
git pull --ff-only origin develop         # 최신 develop 받기 (--ff-only: 기록이 갈라졌으면 멈춤)
git switch -c feature/backend/wpm-api     # 작업 브랜치 생성
```

`backend/app/main.py` 의 `/health` 응답에 `"version": "1"` 같은 값을 추가하고, `tests/test_api.py` 의 기대값도 같이 맞춥니다.

```bash
git add backend/
git commit -m "feat: health 응답에 version 추가"
git push -u origin feature/backend/wpm-api
```

GitHub에 뜨는 **Compare & pull request** → base: `develop`, compare: 내 브랜치 → Create.

확인할 것
- PR 아래 **Checks**: `backend CI / test` → `backend CI / docker` 순서로 ✅
- 상단 **Actions** 탭 → 실행 기록 클릭 → 각 Step을 펼쳐 로그 읽기
- `frontend CI` 는 **실행되지 않음** (frontend 폴더를 안 바꿨으므로)
- 머지 버튼 옆 ▼ → **Squash and merge** → 커밋 메시지 확인 후 머지

머지 후 로컬 정리:

```bash
git switch develop
git pull --ff-only origin develop         # 방금 squash된 커밋 받기
git log --oneline -3                      # 작업 커밋 여러 개가 1개로 들어온 것 확인
git fetch --prune                         # 원격에서 지워진 브랜치의 추적 정보 정리
git branch -d feature/backend/wpm-api     # 거부되면 PR 머지 확인 후 -D
```

## 미션 2. 단위 테스트 실패 (버그를 CI가 잡는 경험)

새 브랜치에서 `backend/app/speech.py` 의 `* 60` 을 `* 30` 으로 바꿔 버그를 만들고 PR.

- 결과: `test` ❌, `docker` 는 **건너뜀** (`needs: test` 때문)
- 로그에서 `assert 75.0 == 150.0` 같은 줄을 찾아보기
- 버그를 고친 커밋을 **같은 브랜치에 push** → PR의 CI가 자동으로 다시 실행 → ✅

## 미션 3. 이미지 빌드 실패

`backend/Dockerfile` 의 `COPY app ./app` 을 `COPY ap ./app` 으로 오타를 내고 PR.

- 결과: `test` ✅ 인데 `docker` ❌ → **테스트 통과 ≠ 빌드 성공**

## 미션 4. 빌드는 되는데 실행이 안 됨

`backend/Dockerfile` 마지막 줄의 `"8000"` 을 `"9000"` 으로 바꾸고 PR.

- 결과: 이미지 빌드 ✅, `/health 응답 확인` ❌ (서버가 다른 포트에서 떠서 응답 없음)
- 로그 끝에 `docker logs` 출력이 남는 것 확인 → **빌드 성공 ≠ 실행 성공**

## 미션 5. paths 필터 확인

`frontend/index.html` 의 문장만 바꿔 PR → `frontend CI` 만 실행되는지 확인.
그다음 `<h1>` 의 "발표 코칭" 문구를 지워 보면 ❌ (검사 조건이 깨짐).

## 미션 6. develop → main (Merge commit)

GitHub에서 **New pull request** → base: `main`, compare: `develop` → Create.
머지 버튼 ▼ → **Create a merge commit** 으로 머지.

> 이 PR은 develop 대상이 아니라서 CI가 돌지 않는 게 정상입니다 (workflow의 `branches: [develop]`).

확인:

```bash
git fetch origin
git log --oneline --graph origin/main -10   # 갈라졌다 합쳐지는 선(merge commit)이 보임
```

미션 1~5를 한 번 더 하고 다시 develop → main PR을 열어, **새로 추가된 것만** 목록에 나오는지 확인합니다.

---

## 내 맥에서 실행해 보기 (Docker Desktop 필요)

```bash
docker compose up --build        # 두 이미지를 빌드하고 실행 (--build: 코드 변경 반영)
# 브라우저: http://localhost:8080 (frontend), http://localhost:8000/health (backend)
# http://localhost:8000/speech-rate?words=150&seconds=60
docker compose down              # 정지 및 컨테이너 삭제
```

## 다음 단계

이 저장소의 두 이미지를 그대로 써서 맥의 k3d(쿠버네티스)에 올려 볼 예정입니다.
