from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import (
    CourseViewSet, LessonListCreateAPIView, LessonRetrieveUpdateDestroyAPIView)


app_name = MaterialsConfig.name

router = SimpleRouter()
router.register('', CourseViewSet, basename='course')

urlpatterns = [
    path('lessons/', LessonListCreateAPIView.as_view(), name='lessons_list'),

    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyAPIView.as_view(),
         name='lessons_retrieve'),

    path('lessons/create/', LessonListCreateAPIView.as_view(),
         name='lessons_create'),

    path('lessons/<int:pk>/update/', LessonRetrieveUpdateDestroyAPIView.as_view(),
        name='lessons_update'),

    path('lessons/<int:pk>/delete/', LessonRetrieveUpdateDestroyAPIView.as_view(),
        name='lessons_delete')
]
urlpatterns += router.urls
