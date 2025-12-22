from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    first_name = models.CharField('Имя', max_length=150,)
    last_name = models.CharField('Фамилия', max_length=150,)
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Никнейм',
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message=(
                    'Никнейм может содержать только буквы,'
                    'цифры и символы @/./+/-/_'
                )
            ),
        ],
    )
    password = models.CharField(
        max_length=300,
        blank=False,
        verbose_name='Пароль пользователя',
    )
    avatar = models.ImageField(
        upload_to='users/images/',
        blank=True,
        default=None,
        verbose_name='Аватар',
    )
    end_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата окончания сбора',
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
