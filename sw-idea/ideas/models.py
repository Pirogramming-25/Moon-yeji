from django.db import models
from django.contrib.auth.models import User
from devtools.models import DevTool

class Idea(models.Model):
    title = models.CharField(max_length=200)        # 제목
    image = models.ImageField(upload_to='ideas/')   # 썸네일 이미지
    content = models.TextField()                    # 내용
    interest = models.IntegerField(default=0)       # 관심도
    devtool = models.ForeignKey(
        DevTool,
        on_delete=models.SET_NULL,
        null=True
    )                                               # 개발툴
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class IdeaStar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'idea')  # 찜 중복 방지

    def __str__(self):
        return f"{self.user.username} - {self.idea.title}"
