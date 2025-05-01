from django.core.validators import URLValidator
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Lesson, Course


class LessonSerializer(ModelSerializer):
    link = serializers.URLField(validators=[URLValidator()])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    count_lessons = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)


    def get_count_lessons(self, course):
        return course.lesson_set.count()

    class Meta:
        model = Course
        fields = ('name', 'preview', 'description', 'count_lessons', 'lessons')