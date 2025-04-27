from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
# from materials.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name='Почта', help_text='Укажите свою почту')
    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name='Телефон',
        help_text='Укажите свой номер телефона')
    city = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Город',
        help_text='Укажите свой город')
    avatar = models.ImageField(
        upload_to='users/avatars',
        blank=True,
        null=True,
        verbose_name='Аватар',
        help_text='Загрузите свой аватар')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
