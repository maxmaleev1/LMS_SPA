from celery import shared_task
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from users.models import User


@shared_task
def check_user_last_login():
    '''Блокирует пользователя, если он не авторизовался в течение 30 дней'''
month_ago = timezone.now() - relativedelta(months=1)
users = User.objects.filter(
    is_active=True,
    last_login__lt=month_ago,
    is_staff=False,
    is_superuser=False
)
users.update(is_active=False)