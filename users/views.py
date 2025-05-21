from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from materials.models import Course
from materials.pagination import CustomPagination
from users.models import Payments, User, Subscription
from users.serializers import PaymentsSerializer, UserSerializer, \
    SubscriptionSerializer
from users.services import create_stripe_product, create_stripe_price, \
    create_stripe_session


class PaymentsViewSet(ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method',)
    ordering_fields = ('payment_date',)
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product = payment.course.name if payment.course else payment.lesson.name
        stripe_product = create_stripe_product(product)
        price = create_stripe_price(payment.payment_sum, stripe_product)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ['create', 'login']:
            self.permission_classes = [AllowAny,]
        return super().get_permissions()

class TokenObtainPairView():
    permission_classes = (AllowAny,)


class TokenRefreshView():
    permission_classes = (AllowAny,)


class SubscriptionCreateAPIView(CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "подписка добавлена"
        return Response({"message": message})
