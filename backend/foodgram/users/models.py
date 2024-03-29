from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    GUEST = 'guest'
    USER = 'user'
    ADMIN = 'admin'
    ACCESS_ROLES = [
        (GUEST, 'guest'),
        (USER, 'user'),
        (ADMIN, 'administrator'),
    ]

    email = models.EmailField(
        max_length=254,
        blank=False,
        null=False,
        unique=True,
        verbose_name='Адрес электронной почты'
    )
    username = models.CharField(
        max_length=150,
        null=False,
        blank=False,
        unique=True,
        verbose_name='Никнейм'
    )
    first_name = models.CharField(
        max_length=150,
        null=False,
        blank=False,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        null=False,
        blank=False,
        verbose_name='Фамилия'
    )
    password = models.CharField(
        max_length=150,
        null=False,
        blank=False,
        verbose_name='Пароль'
    )
    role = models.CharField(
        max_length=50,
        null=True,
        choices=ACCESS_ROLES,
        verbose_name='Уровень доступа',
        default=GUEST
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['-id']


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} подписан на {self.author}"

    class Meta:
        ordering = ['-id']
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_users',
            ),)
