from django.contrib import admin
from . import models


@admin.register(models.Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "is_active", "get_jalali_date")
    list_editable = ("is_active",)
    list_filter = ("created_at", "updated_on")
    search_fields = ("title", "about_video")


@admin.register(models.Category)
class CateAdmin(admin.ModelAdmin):
    list_display = ("__str__", "get_jalali_date")
    list_filter = ("created_at",)
    search_fields = ("title",)
    prepopulated_field = {'slug': ('title',)}


@admin.register(models.SubCategory)
class CateAdmin(admin.ModelAdmin):
    list_display = ("__str__", "get_jalali_date")
    list_filter = ("created_at",)
    search_fields = ("title",)


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "is_active", "get_date")
    list_editable = ("is_active",)
    list_filter = ("created_at",)
    search_fields = ("title",)
    actions = ['is_active']


@admin.register(models.Like)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
    list_filter = ("created_at", "video")


@admin.register(models.Favorite)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("__str__",)

