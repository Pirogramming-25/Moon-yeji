from django.db import models

class Review(models.Model):
    title = models.CharField(max_length=100)        # 영화 제목
    director = models.CharField(max_length=50)       # 감독
    actor = models.CharField(max_length=100)         # 주연
    genre = models.CharField(max_length=50)           # 장르
    release_year = models.IntegerField()              # 개봉년도
    rating = models.FloatField()                      # 별점
    running_time = models.IntegerField()               # 러닝타임(분)
    content = models.TextField()                       # 리뷰 내용

    def __str__(self):
        return self.title