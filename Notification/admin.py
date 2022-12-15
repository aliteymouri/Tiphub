from django.contrib import admin
from . import models

admin.site.register(models.GeneralNotification)


@admin.register(models.PersonalNotification)
class AdminPersonalNotification(admin.ModelAdmin):
    list_display = ("__str__", "sender")
    list_filter = ("created_at", "sender")
    search_fields = ("user",)
