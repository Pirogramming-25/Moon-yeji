from django.db import models

class DevTool(models.Model):
    name = models.CharField(max_length=100)    # 이름
    kind = models.CharField(max_length=100)    # 분류
    content = models.TextField()               # 설명

    def __str__(self):
        return self.name