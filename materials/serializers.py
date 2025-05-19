from materials.validators import URLValidator
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from materials.models import Lesson, Course
from users.models import Subscription


class LessonSerializer(ModelSerializer):
    link = serializers.URLField(validators=[URLValidator()])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    count_lessons = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    subscription = SerializerMethodField()

    def get_count_lessons(self, course):
        return course.lesson_set.count()

    def get_subscription(self, course):
        user = self.request.user
        subscription = Subscription.objects.filter(user=user, course=course)
        if subscription:
            return subscription.is_active
        else:
            return False

    class Meta:
        model = Course
        fields = (
            'name', 'preview', 'description', 'count_lessons', 'lessons',
            'subscription'
        )