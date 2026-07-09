from django.contrib import admin
from .models import Post, Comment, Like, Story, StoryImage, Follow, Profile

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Story)
admin.site.register(StoryImage)
admin.site.register(Follow)
admin.site.register(Profile)