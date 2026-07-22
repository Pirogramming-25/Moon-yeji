# Django GPT

Hugging Face 모델을 Django 웹 서비스로 구성한 AI 웹 애플리케이션입니다.

## 🧰 기술 스택

- Django 5.2
- Hugging Face Transformers (`pipeline()`)
- python-dotenv
- HTML / CSS / JavaScript (Fetch API)

## 📦 구현 기능

| 탭             | URL           | 접근 권한     |
| -------------- | ------------- | ------------- |
| 감정 분석      | `/sentiment/` | 비로그인 허용 |
| 문서 요약      | `/summarize/` | 로그인 필요   |
| 유해 표현 분석 | `/moderate/`  | 로그인 필요   |

## 🤖 사용 모델

### 1. 감정 분석

- **Model ID**: `cardiffnlp/twitter-roberta-base-sentiment-latest`
- **License**: Apache-2.0
- **입력 언어**: 영어
- **출력 레이블**: `negative`, `neutral`, `positive`

### 2. 문서 요약

- **Model ID**: `sshleifer/distilbart-cnn-6-6`
- **License**: Apache-2.0
- **입력 언어**: 영어
- **출력**: 요약문, 원문/요약문 길이, 요약 비율

### 3. 유해 표현 분석

- **Model ID**: `unitary/toxic-bert`
- **License**: Apache-2.0
- **입력 언어**: 영어
- **출력 레이블**: `toxic`, `severe_toxic`, `obscene`, `threat`, `insult`, `identity_hate` (Multi-label)

## ⚙️ 실행 방법

### 1. 저장소 클론

```bash
git clone <repository-url>
cd Django_GPT
```

### 2. 가상환경 생성 및 활성화

```bash
python -m venv venv

# Windows (Git Bash)
source venv/Scripts/activate

# Mac/Linux
source venv/bin/activate
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. 환경변수 설정

`.env.example`을 참고하여 `.env` 파일을 생성합니다.

### 5. 데이터베이스 마이그레이션

```bash
python manage.py migrate
```

### 6. 관리자 계정 생성 (로그인 테스트용)

```bash
python manage.py createsuperuser
```

### 7. 서버 실행

```bash
python manage.py runserver
```

브라우저에서 `http://127.0.0.1:8000/sentiment/` 접속

## 🔐 환경변수 설명

| 변수명       | 설명                                              |
| ------------ | ------------------------------------------------- |
| `SECRET_KEY` | Django 프로젝트의 비밀 키 (직접 발급받은 값 사용) |
| `DEBUG`      | 디버그 모드 여부 (`True`/`False`)                 |

## 📁 프로젝트 구조
