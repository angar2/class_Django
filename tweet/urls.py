# tweet/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), # 127.0.0.1:8000과 views.py 폴더의 home 함수 연결
    path('tweet/', views.tweet, name='tweet'),
    path('tweet/delete/<int:id>', views.delete_tweet, name='delete-tweet'),
]