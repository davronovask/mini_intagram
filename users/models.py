from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models
from users.managers import AccountManager


class Account(AbstractUser):
    """Модель для аккаунта"""

    username = models.CharField(
        max_length=30,
        validators=[MinLengthValidator(4)],
        unique=True,
        db_index=True, # добавляет индекс для данной таблицы, чтобы делать поиск по имейлу быстрее)
        )
    avatar = models.ImageField(
        upload_to="avatars/",
        null=True, # Это поле может быть пустым как на уровне базы данных)
        blank=True, # Этот параметр указывает, что поле может быть оставлено пустым в формах Django)
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = AccountManager()

    class Meta:
        verbose_name_plural = 'Аккаунты'
        verbose_name = 'Аккаунт'


class AccountFollower(models.Model):
    following = models.ForeignKey(
        Account,
        verbose_name='на кого подписался',
        on_delete=models.CASCADE,
        related_name='my_followers',
    )

    follower = models.ForeignKey(
        Account,
        verbose_name='кто подписался',
        on_delete=models.CASCADE,
        related_name='my_following',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('following', 'follower')  # Ограничиваем, чтобы один и тот же пользователь не мог подписываться дважды
        verbose_name_plural = 'Подписки'
        verbose_name = 'Подписка'