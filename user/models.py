#user/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings # 메인앱의 settings.py를 불러옴

# Create your models here.
class UserModel(AbstractUser):
    class Meta:
        db_table = "my_user"

    bio = models.CharField(max_length=256, default='')
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followee') # 상대 데이터베이스에는 followee로 들어감