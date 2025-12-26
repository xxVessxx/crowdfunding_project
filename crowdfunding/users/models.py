from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    first_name = models.CharField('Имя', max_length=150,)
    last_name = models.CharField('Фамилия', max_length=150,)
    middle_name = models.CharField('Отчество', max_length=150,)
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
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['middle_name', 'first_name', 'last_name']

    class Meta:
        ordering = ['email']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_full_name_custom(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    def __str__(self):
        return self.get_full_name_custom()
