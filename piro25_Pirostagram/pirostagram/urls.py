from django.urls import path
from . import views

app_name = 'pirostagram'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('post/create/', views.post_create_view, name='post_create'),
    path('post/<int:post_id>/edit/', views.post_edit_view, name='post_edit'),
    path('post/<int:post_id>/delete/', views.post_delete_view, name='post_delete'),
    path('post/<int:post_id>/like/', views.post_like_view, name='post_like'),
    path('post/<int:post_id>/comment/', views.comment_create_view, name='comment_create'),
    path('comment/<int:comment_id>/edit/', views.comment_edit_view, name='comment_edit'),
    path('comment/<int:comment_id>/delete/', views.comment_delete_view, name='comment_delete'),
    path('search/', views.user_search_view, name='user_search'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('follow/<str:username>/', views.follow_toggle_view, name='follow_toggle'),
    path('story/create/', views.story_create_view, name='story_create'),
    path('story/<str:username>/view/', views.story_view, name='story_view'),
]