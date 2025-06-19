from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from users.models import Payments, Subscription
from users.models import User


class PaymentsSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
