from django.shortcuts import render
from django.http import JsonResponse
from celery.result import AsyncResult
from .models import FakeNews  # FakeNews 모델을 만들어야 함
from .tasks import generate_fake_news
import datetime

# main 페이지를 렌더링하는 뷰
def main(request):
    return render(request, 'main/main.html')

def generate_news(request):
    # 버튼 클릭 시 가장 최신 뉴스를 즉시 반환하고, 없으면 Celery 실행
    latest_news = FakeNews.objects.order_by('-created_at').first()

    # 1시간 이내 생성된 뉴스가 있으면 즉시 반환
    if latest_news and (datetime.datetime.now() - latest_news.created_at).seconds < 3600:
        return JsonResponse({'status': 'Completed', 'result': latest_news.content})
    
    # 뉴스가 없거나 너무 오래된 경우, 새로운 뉴스 생성 요청
    task = generate_fake_news.apply_async()
    return JsonResponse({'task_id': task.id})

def generate_news_view(request):
    task = generate_fake_news.apply_async()
    return render(request, 'news/generateNews.html', {'task_id': task.id})


def check_task_status(request, task_id):
    task_result = AsyncResult(task_id)
    if task_result.ready():
        return JsonResponse({'status': 'Completed', 'result': task_result.result})
    else:
        return JsonResponse({'status': 'Pending'})