from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy
from . import views

app_name = 'account'
urlpatterns = [
    path('sign_in', views.SignInView.as_view(), name='sign_in'),
    path('sign_up', views.SignUpView.as_view(), name='sign_up'),
    path('activate/<uidb64>/<token>', views.Activate.as_view(), name='activate'),
    path('logout', LogoutView.as_view(next_page='account:sign_in'), name='logout'),
    path('userpanel', views.UserPanelView.as_view(), name='user_panel'),
    path('editprofile', views.EditProfileView.as_view(), name='edit_profile'),
    path('change/password', views.ChangePasswordView.as_view(), name='change_password'),

    path('reset_password', views.ResetPasswordView.as_view(), name='reset_password'),
    path('password_reset_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="passwords/password_reset_send.html"),
         name="password_reset_send"),
    path('reset_password/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset.html",
                                                     success_url=reverse_lazy('account:password_reset_complete')),
         name="password_reset_confirm"),
    path('reset_password/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="passwords/password_reset_done.html"),
         name="password_reset_complete"),
]
