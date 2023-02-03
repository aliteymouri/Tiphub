from rest_framework import serializers
from Account.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['is_active', 'is_admin', 'is_staff', 'date_joined']
