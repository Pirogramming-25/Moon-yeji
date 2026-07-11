# 베이스 이미지
FROM python:3.12

# 작업 디렉토리 설정
WORKDIR /app

# requirements 먼저 복사 (레이어 캐싱)
COPY requirements.txt .

# 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 나머지 전체 파일 복사
COPY . .

# 8000번 포트 사용 명시
EXPOSE 8000

# 컨테이너 실행 시 명령어
CMD python manage.py migrate --noinput && \
    python manage.py runserver 0.0.0.0:8000