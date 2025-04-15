from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    last_login = models.DateTimeField(null=True, blank=True)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    telegram_username = models.CharField(max_length=30, blank=True, null=True)


class Follow(models.Model):

    # Это внешний ключ — связь с другой таблицей. В данном случае — с user
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='following',
        on_delete=models.CASCADE
    )

    # related_name='followers' ---> user.following.all() ; user.followers.all()
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='followers',
        on_delete=models.CASCADE
    )

    # Этот столбец будет хранить дату и время создания записи
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Это ограничение уникальности на уровне базы данных.
        unique_together = ('follower', 'following')

    def __str__(self):
        # в админке и в консоли
        return f"{self.follower} → {self.following}"
