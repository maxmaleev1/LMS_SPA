from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, \
    TokenRefreshView

from users.apps import UsersConfig
from users.views import PaymentsViewSet, UserViewSet

app_name = UsersConfig.name

router = SimpleRouter()
router.register(r'payments', PaymentsViewSet, basename='payments')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls