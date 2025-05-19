import django
from django.conf import settings

if not settings.configured:
    django.setup()


import json
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from materials.models import Course, Lesson
from users.models import Subscription, User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user, created = User.objects.get_or_create(email='admin@email.com')
        self.course = Course.objects.create(
            name='Курс Тест Имя',
            description='Курс Тест Описание'
        )
        self.lesson = Lesson.objects.create(
            name='Урок Тест',
            course=self.course,
            owner=self.user,
            link='https://www.youtube.com/',
        )
        self.client.force_authenticate(user=self.user)
        moderators_group, created = Group.objects.get_or_create(
            name='Модераторы'
        )
        self.user.groups.add(moderators_group)

    def test_lesson_retrieve(self):
        url = reverse(
            'materials:lessons_retrieve_update_destroy',
            args=(self.lesson.pk,)
        )
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), self.lesson.name)

    def test_lesson_create(self):
        url = reverse('materials:lessons_list_create')
        data = {
            'name': 'Урок Тест 2',
            'course': self.course.pk,
            'link': 'https://www.youtube.com/',
        }
        response = self.client.post(
            url, json.dumps(data), content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse(
            'materials:lessons_retrieve_update_destroy',
            args=(self.lesson.pk,)
        )
        data = {'name': 'Урок Тест Обновлен'}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), 'Урок Тест Обновлен')

    def test_lesson_delete(self):
        url = reverse(
            'materials:lessons_retrieve_update_destroy',
            args=(self.lesson.pk,)
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse('materials:lessons_list_create')
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [{
                    "id": self.lesson.pk,
                    "link": self.lesson.link,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "preview": None,
                    "course": self.course.pk,
                    "owner": self.user.pk,
            }],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class LessonUnauthorizedTestCase(APITestCase):

    def setUp(self):
        self.course = Course.objects.create(
            name='Курс Тест Имя',
            description='Курс Тест Описание')
        self.lesson = Lesson.objects.create(
            name='Урок 1',
            course=self.course,
            link='https://www.youtube.com/',
        )

    def test_lesson_retrieve(self):
        url = reverse(
            'materials:lessons_retrieve_update_destroy',
            args=(self.lesson.pk,)
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_update(self):
        url = reverse(
            'materials:lessons_retrieve_update_destroy',
            args=(self.lesson.pk,)
        )
        data = {'name': 'Тест 1'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_delete(self):
        url = reverse(
            'materials:lessons_retrieve_update_destroy',
            args=(self.lesson.pk,)
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_list(self):
        url = reverse('materials:lessons_list_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user, created = User.objects.get_or_create(email='admin@email.com')
        self.course = Course.objects.create(
            name='Тест',
            description='Тест'
        )
        self.client.force_authenticate(user=self.user)

    def test_subscription(self):
        url = reverse('users:subscription')
        data = {'course': self.course.pk}
        response = self.client.post(url, data)
        data = response.json()
        message = {'message': 'подписка добавлена'}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, message)
        self.assertEqual(Subscription.objects.all().count(), 1)

        data = {'course': self.course.pk}
        response = self.client.post(url, data)
        data = response.json()
        message = {'message': 'подписка удалена'}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, message)
        self.assertEqual(Subscription.objects.all().count(), 0)
