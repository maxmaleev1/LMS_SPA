from django.db import models


class Course(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название курса',
        help_text='Укажите название курса')

    preview = models.ImageField(
        upload_to='materials/preview',
        blank=True,
        null=True,
        verbose_name='Превью',
        help_text='Загрузите превью курса')

    description = models.TextField(
        verbose_name='Описание курса',
        blank=True,
        null=True,
        help_text='Укажите описание курса')

    lessons = models.ManyToManyField('Lesson', verbose_name='Уроки')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название урока',
        help_text='Укажите название урока')

    description = models.TextField(
        verbose_name='Описание урока',
        blank=True,
        null=True,
        help_text='Укажите описание урока')

    preview = models.ImageField(
        upload_to='materials/preview',
        blank=True,
        null=True,
        verbose_name='Превью',
        help_text='Загрузите превью урока')

    link = models.URLField(
        verbose_name='Ссылка на урок',
        help_text='Добавьте ссылку на урок',
        blank=True,
        null=True)

    courses = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name='Курс',
        help_text='Укажите курс',
        blank=True,
        null=True)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
