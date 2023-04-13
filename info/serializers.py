from rest_framework import serializers
from .models import BeTeacher


class BeTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeTeacher
        fields = "__all__"
