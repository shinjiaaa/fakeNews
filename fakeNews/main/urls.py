from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),  # 홈 페이지 URL
    path('generate_news/', views.generate_news_view, name='generate_news'),  # 비동기 작업 시작
    path('<str:task_id>/', views.check_task_status, name='check_task_status'),  # 작업 상태 확인
]
