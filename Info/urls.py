from django.urls import path
from . import views

app_name = "info"
urlpatterns = [
    path("about_us", views.AboutUsView.as_view(), name="about_us"),
    path("be_teacher", views.BeTeacherView.as_view(), name="be_teacher"),
]
