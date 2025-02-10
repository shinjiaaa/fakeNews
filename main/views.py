from django.shortcuts import render
from django.http import JsonResponse
from celery.result import AsyncResult
from .models import fakeVerse  # fakeVerse 모델을 만들어야 함
from .tasks import generate_fake_news
import datetime
import google.generativeai as genai
import os

# API 키 가져오기
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY 환경 변수가 설정되지 않았습니다.")

# Google Generative AI 클라이언트 설정
genai.configure(api_key=GOOGLE_API_KEY)

# 모델 설정
model = "gemini-1.5-flash-001"


# main 페이지를 렌더링하는 뷰
def main(request):
    return render(request, "main/main.html")


# 가짜 뉴스를 생성하는 뷰
def generate_news(request):
    try:
        # 버튼 클릭 시 가장 최신 뉴스를 즉시 반환하고, 없으면 Celery 실행
        latest_news = fakeVerse.objects.order_by("-created_at").first()

        # 1시간 이내 생성된 뉴스가 있으면 즉시 반환
        if (
            latest_news
            and (datetime.datetime.now() - latest_news.created_at).seconds < 3600
        ):
            return JsonResponse({"status": "Completed", "result": latest_news.content})

        # 뉴스가 없거나 너무 오래된 경우, 새로운 뉴스 생성 요청
        topic = "기술"  # 예시로 '기술'을 주제로 설정
        task = generate_fake_news.apply_async(args=[topic])  # topic을 인자로 전달
        return JsonResponse({"task_id": task.id})

    except Exception as e:
        # 예외를 문자열로 변환하여 JsonResponse로 반환
        return JsonResponse({"error": str(e)})


# 가짜 뉴스를 생성하는 뷰 (직접 처리 방식)
def generate_news_view(request):
    try:
        # 주어진 topic을 바탕으로 뉴스 생성 프롬프트 설정
        topic = "기술"  # 예시로 '기술'을 주제로 설정
        prompt = f"{topic}에 관한 최신 뉴스"

        # Google Generative AI로부터 뉴스 생성
        response = genai.generate(
            prompt=prompt,
            model=model,
            max_output_tokens=200,
        )

        # 생성된 뉴스 내용
        fake_news_content = response.text

        # 생성된 뉴스 내용을 DB에 저장
        # fake_news = fakeVerse.objects.create(content=fake_news_content)///

        # 생성된 뉴스 내용을 반환
        return JsonResponse({"status": "Completed", "result": fake_news_content})

    except Exception as e:
        # 예외를 문자열로 변환하여 JsonResponse로 반환
        return JsonResponse({"error": str(e)})


# 가짜 뉴스 상태를 확인하는 뷰
def check_task_status(request, task_id):
    try:
        task_result = AsyncResult(task_id)
        if task_result.ready():
            return JsonResponse({"status": "Completed", "result": task_result.result})
        else:
            return JsonResponse({"status": "Pending"})
    except Exception as e:
        # 예외를 문자열로 변환하여 JsonResponse로 반환
        return JsonResponse({"error": str(e)})
