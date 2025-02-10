import google.generativeai as genai
from celery import shared_task
from django.conf import settings
from .models import fakeVerse

# 구글 Generative AI 설정
genai.configure(api_key=settings.GOOGLE_API_KEY)


@shared_task
def generate_fake_news(topic):
    try:
        # 주어진 topic을 바탕으로 뉴스 생성 프롬프트 설정
        prompt = f"{topic}에 관한 최신 뉴스"

        # Generative AI로부터 뉴스 생성
        response = genai.generate_text(prompt=prompt, max_output_tokens=500)

        # 생성된 뉴스 내용
        fake_news_content = (
            response.text
        )  # 이 부분은 'response.result' 대신 'response.text'로 변경 가능

        # 생성된 뉴스 내용을 DB에 저장
        fake_news = fakeVerse.objects.create(content=fake_news_content)

        # 생성된 뉴스 내용을 반환
        return fake_news_content, fake_news

    except Exception as e:
        return f"뉴스 생성 중 오류 발생: {str(e)}"
