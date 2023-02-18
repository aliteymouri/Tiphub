from django.urls import path
from . import views

app_name = "info"
urlpatterns = [
    path("about_us", views.AboutUsView.as_view(), name="about_us"),
    path("be_teacher", views.BeTeacherView.as_view(), name="be_teacher"),
    path("teachers", views.TeachersView.as_view(), name="teachers"),
    path('why_tiphub', views.WhyTipHubView.as_view(), name='why_tiphub'),
    path('privacy_policy', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
]
