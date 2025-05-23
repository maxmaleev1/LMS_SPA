from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from materials.models import Course, Lesson
from materials.pagination import CustomPagination
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsOwner, IsModer
from users.tasks import sendmail_course_updated


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action == ["create", "destroy",]:
            self.permission_classes = (IsOwner,)
        elif self.action in ["retrieve", "update"]:
            self.permission_classes = (IsModer | IsOwner,)
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def perform_update(self, serializer):
        updated_course = serializer.save()
        sendmail_course_updated.delay(updated_course)
        updated_course.save()


class LessonListCreateAPIView(ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModer, IsAuthenticated,)
    pagination_class = CustomPagination

class LessonRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination
