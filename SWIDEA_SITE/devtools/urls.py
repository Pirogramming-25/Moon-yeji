from django.urls import path
from . import views

urlpatterns = [
    path('', views.devtool_list, name='devtool_list'),
    path('new/', views.devtool_form, name='devtool_form'),
    path('<int:pk>/', views.devtool_detail, name='devtool_detail'),
    path('<int:pk>/update/', views.devtool_update, name='devtool_update'),
    path('<int:pk>/delete/', views.devtool_delete, name='devtool_delete'),
]