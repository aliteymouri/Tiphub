from django.urls import path
from . import views

app_name = 'notification'
urlpatterns = [
    path("DelNotif/<int:pk>", views.RemoveNotification.as_view(), name='remove_per_notification'),
    path("DelAdmin/<int:pk>", views.RemoveAdminNotification.as_view(), name='remove_ad_notification'),
    path("Notifications/", views.Notifications.as_view(), name='notifications'),
]

