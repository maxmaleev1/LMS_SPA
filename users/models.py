from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from materials.models import Course, Lesson


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


class Payments(models.Model):
    CASH = 'cash'
    TRANSFER = 'transfer'

    CHOICE_PAY_METHOD = [(CASH, 'Наличные'), (TRANSFER, 'Перевод на счет'),]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name='Пользователь',
        blank=True,
        null=True)

    payment_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата оплаты',
        help_text='Введите дату оплаты')

    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name='Курс',
        blank=True,
        null=True)

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        verbose_name='Урок',
        blank=True,
        null=True)

    payment_amount = models.PositiveIntegerField(
        verbose_name='Сумма оплаты',
        blank=True,
        null=True)

    payment_method = models.CharField(
        max_length=10, choices=CHOICE_PAY_METHOD, verbose_name='Способ оплаты')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return (f'{self.user} оплачены урок(-и) - {self.lesson},'
                f'курс(-ы) - {self.course}')


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name='Пользователь',
        blank=True,
        null=True,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name='Подписка на курс',
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='Статус подписки')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
