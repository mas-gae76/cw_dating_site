from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from PIL import Image
from django.conf import settings
from .utils import get_timestamp_path_user


class User(AbstractUser):

    class Gender(models.TextChoices):
        __empty__ = 'Укажите Ваш пол'
        MALE = 'М', 'Мужской'
        FEMALE = 'Ж', 'Женский'

    id = models.UUIDField(primary_key=True, default=uuid4, null=False)
    first_name = models.CharField(verbose_name='Имя', max_length=40)
    last_name = models.CharField(verbose_name='Фамилия', max_length=40)
    username = models.CharField(blank=True, verbose_name='Никнейм', max_length=10)
    email = models.EmailField(verbose_name='Email', unique=True, max_length=128)
    birthday = models.DateField(verbose_name='Дата рождения')
    description = models.CharField(verbose_name='Описание', max_length=150, null=True)
    avatar = models.ImageField(verbose_name='Фото', default=None, upload_to=get_timestamp_path_user, blank=True)
    gender = models.CharField(max_length=1, verbose_name='Пол', choices=Gender.choices, default=None)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        super().save()
        if self.avatar:
            avatar = Image.open(self.avatar.path)
            watermark = Image.open(settings.WATERMARK_PATH)
            watermark.thumbnail((100, 100))
            x = avatar.size[0] - watermark.size[0] - 20
            y = avatar.size[1] - watermark.size[1] - 20
            avatar.paste(watermark, (x, y), mask=watermark)
            avatar.save(self.avatar.path)

    def __str__(self):
        return f'Участник {self.first_name} {self.last_name}: {self.email}'

    class Meta:
        verbose_name_plural = 'Участники'
        verbose_name = 'Участник'
        ordering = ['last_name']


class UserRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(verbose_name='Рейтинг')

    class Meta:
        verbose_name = 'Рейтинг пользователей'
        verbose_name_plural = 'Рейтинги пользователей'


class Settings(models.Model):
    name = models.CharField(verbose_name='Настройка', max_length=30)

    class Meta:
        verbose_name_plural = 'Настройки'
        verbose_name = 'Настройка'


class UserSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    setting = models.ForeignKey(Settings, on_delete=models.PROTECT)
    value = models.IntegerField(verbose_name='Значение настройки', default=0)

    class Meta:
        verbose_name_plural = 'Пользовательские настройки'


class Sympathy(models.Model):
    who = models.ForeignKey(User, on_delete=models.CASCADE, related_name='who')
    whom = models.ForeignKey(User, on_delete=models.CASCADE, related_name='whom')
    matching = models.BooleanField(verbose_name='Взаимно?', default=False)

    def __str__(self):
        return f'{self.who} оценил {self.whom}'

    class Meta:
        verbose_name = 'Взаимная симпатия'
        constraints = [models.UniqueConstraint(fields=('who', 'whom'), name='unique_matching')]