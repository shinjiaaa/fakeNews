import google.generativeai as genai
from celery import shared_task
from .models import fakeVerse
import os
from django.core.cache import cache

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY 환경 변수가 설정되지 않았습니다.")

genai.configure(api_key=GOOGLE_API_KEY)


@shared_task
def generate_fake_news(topic):
    # 캐시에서 이미 결과가 있는지 확인
    cached_result = cache.get(topic)
    if cached_result:
        return cached_result

    # 구글 AI 호출 (캐시 미사용 시)
    prompt = f"{topic}에 관한 최신 뉴스"
    response = genai.generate(prompt=prompt, model="gemini-1.5-flash-001", max_output_tokens=200)
    
    fake_news_content = response.text
    # 캐시 저장 (5분 동안 캐시)
    cache.set(topic, fake_news_content, timeout=300)

    return fake_news_content
