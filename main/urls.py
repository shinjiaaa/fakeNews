from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.main, name="main"),  # 메인
    path("generate_news/", views.generate_news_view, name="generate_news"),  # 뉴스 생성
    path(
        "task_status/<str:task_id>/", views.check_task_status, name="check_task_status"
    ),  # 생성된 뉴스 확인
    path("chatbot/", include("chatbot.urls")),
    path("tutorial/", include("tutorial.urls")),
]
