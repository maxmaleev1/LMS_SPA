from celery import shared_task
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from users.models import Subscription, User


@shared_task
def sendmail_course_updated(course):
    '''Отправляет уведомление о том, что курс обновлен'''
    subscription_course = Subscription.objects.filter(course=course)
    for subscription in subscription_course:
        print(f'Отправляем уведомление на почту {subscription.user.email}')
        send_mail(
            subject='Обновление курса',
            message=f'Курс {subscription.course.name}, на который Вы подписаны, обновился!',
            from_email=EMAIL_HOST_USER,
            recipient_list=[subscription.user.email],
            fail_silently=False,
        )
