from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):

    USER = 'user'
    ADMIN = 'admin'

    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
    )

    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        verbose_name='email'
    )
    password = models.CharField(
        max_length=150,
        default='password',
        verbose_name='Пароль',
        blank=False
    )
    bio = models.TextField(
        blank=True,
        verbose_name='био'
    )
    confirmation_code = models.CharField(
        max_length=20,
        default='0000',
        blank=True,
        null=True,
        verbose_name='Код'
    )
    role = models.CharField(
        max_length=16,
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name='Роль'
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[RegexValidator(r'^[\w.@+-]+'), ]
    )
    is_subscribed = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_user(self):
        return self.role == self.USER

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique_username_email'
            )
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписан'
    )

    class Meta:
        verbose_name = 'Подписка на авторов'
        verbose_name_plural = 'Подписки на авторов'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_subscribe'
            )
        ]

    def __str__(self):
        return f'{self.user.username} подписан на {self.author.username}'
