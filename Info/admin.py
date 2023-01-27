from django.contrib import admin
from .models import BeTeacher


@admin.register(BeTeacher)
class BeTeacherAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        if user.is_superuser or user.is_CSO or user.is_CSO:
            return qs
        return None
