from django.db import models


class fakeVerse(models.Model):
    content = models.TextField()  # 뉴스 내용 저장을 위한 텍스트 필드
    created_at = models.DateTimeField(auto_now_add=True)  # 생성된 시간 저장
