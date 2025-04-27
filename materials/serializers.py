from django.core.validators import URLValidator
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from materials.models import Lesson, Course


class LessonSerializer(ModelSerializer):
    link = serializers.URLField(validators=[URLValidator()])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(source='lesson_set', many=True)

    class Meta:
        model = Course
        fields = '__all__'