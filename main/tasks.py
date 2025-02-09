import google.generativeai as genai
from celery import shared_task
from django.conf import settings
from .models import fakeVerse
import random

# 구글 Generative AI 설정
genai.configure(api_key=settings.GOOGLE_API_KEY)


@shared_task
def generate_fake_news(topic):
    # 가짜 뉴스 생성 로직
    fake_news_content = f"{topic} 관련 가짜 뉴스 내용: {random.randint(1000, 9999)}"

    # 가짜 뉴스 저장
    fake_news = fakeVerse.objects.create(content=fake_news_content)

    return fake_news_content
