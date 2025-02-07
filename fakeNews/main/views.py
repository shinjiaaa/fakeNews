from django.shortcuts import render
from django.http import JsonResponse
from celery.result import AsyncResult
from .tasks import generate_fake_news  # 생성한 비동기 작업 import

# main 페이지를 렌더링하는 뷰
def main(request):
    return render(request, 'main/main.html')

# 가짜 뉴스 생성 요청을 처리하는 뷰
def generate_news_view(request):
    # 비동기 작업 호출
    task = generate_fake_news.delay()  # 비동기 호출
    return JsonResponse({'message': '가짜 뉴스 생성에 성공하였습니다.', 'task_id': task.id})

# 작업 상태를 확인하는 뷰
def check_task_status(request, task_id):
    task_result = AsyncResult(task_id)
    if task_result.ready():
        result = task_result.result
        return JsonResponse({'task_id': task_id, 'status': '생성 성공', 'result': result})
    else:
        return JsonResponse({'task_id': task_id, 'status': 'In Progress'})
