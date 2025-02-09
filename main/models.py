from django.db import models


class fakeVerse(models.Model):
    content = models.TextField()  # 생성된 뉴스 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 날짜
