from django.urls import path
from . import views

urlpatterns = [
    path('review/', views.review_list, name='review-list'),
    path('review/create/', views.review_create, name='review-create'),
    path('review/<int:pk>/', views.review_detail, name='review-detail'),
    path('review/<int:pk>/update/', views.review_update, name='review-update'),
    path('review/<int:pk>/delete/', views.review_delete, name='review-delete'),
]