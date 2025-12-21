from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Collect(models.Model):
    """Модель группового сбора."""

    OCCASION_CHOICES = (
        ('birthday', 'День рождения'),
        ('wedding', 'Свадьба'),
        ('other', 'Другое'),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='collections',
        verbose_name='Автор',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    occasion = models.CharField(
        max_length=50,
        choices=OCCASION_CHOICES,
        verbose_name='Выбор повода'
    )
    description = models.TextField('Описание')
    target_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Конечная сумма',
    )
    collected_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='Собранная сумма',
    )
    image = models.ImageField(
        upload_to='collects/images/',
        verbose_name='Изображение',
    )
    end_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата окончания сбора',
    )
