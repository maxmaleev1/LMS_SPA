from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import (
    CourseViewSet, LessonListCreateAPIView, LessonRetrieveUpdateDestroyAPIView)


app_name = MaterialsConfig.name

router = SimpleRouter()
router.register('', CourseViewSet, basename='course')

urlpatterns = [
    path('lessons/', LessonListCreateAPIView.as_view()),

    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyAPIView.as_view())
]
urlpatterns += router.urls
