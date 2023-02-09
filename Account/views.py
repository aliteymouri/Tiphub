from .forms import SignInForm, SignUpForm, EditProfileForm, ChangePasswordForm, ResetPasswordForm
from django.contrib.auth.views import PasswordResetView, PasswordChangeView
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .mixins import RequiredLoginMixin, AuthenticatedMixin
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .tokens import account_activation_token
from django.views.generic import CreateView
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from django.views import View
from .models import User


class SignInView(AuthenticatedMixin, View):
    template_name = 'account/sign_in.html'
    form_class = SignInForm

    def get(self, req):
        form = self.form_class()
        return render(req, self.template_name, {'form': form})

    def post(self, req):
        form = self.form_class(req.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None:
                login(req, user)
                return redirect('account:user_panel')
            else:
                form.add_error('email', 'کاربری با مشخصات وارد شده یافت نشد')
        return render(req, self.template_name, {'form': form})


class SignUpView(AuthenticatedMixin, CreateView):
    template_name = 'account/sign_up.html'
    form_class = SignUpForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        current_site = get_current_site(self.request)
        mail_subject = 'لینک فعالسازی حساب کاربری'
        message = render_to_string('emails/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return render(self.request, 'emails/email_confirmation.html')

    def get(self, *args, **kwargs):
        return super(SignUpView, self).get(*args, **kwargs)


class Activate(View):
    def get(self, req, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):

            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(req, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(req, 'emails/email_confirmation_done.html')
        else:
            return HttpResponse("لینک وارد شده منقضی شده است لطفا دوباره تلاش کنید")


class UserPanelView(RequiredLoginMixin, View):
    def get(self, req):
        return render(req, 'account/user_panel.html', {'instance': req.user})


class EditProfileView(RequiredLoginMixin, View):
    form_class = EditProfileForm
    template_name = 'account/edit_profile.html'

    def get(self, req):
        form = self.form_class(instance=req.user)
        return render(req, self.template_name, {"form": form})

    def post(self, req):
        form = self.form_class(req.POST, req.FILES, instance=req.user)
        if form.is_valid():
            form.save()
        else:
            for field in form:
                if field.errors:
                    err_msg = field.errors
                    return JsonResponse({'response': err_msg})
        return render(req, self.template_name)


class ResetPasswordView(PasswordResetView):
    template_name = "account/forgot_password.html"
    email_template_name = "passwords/password_reset_email.html"
    success_url = reverse_lazy('account:password_reset_send')
    form_class = ResetPasswordForm

    def form_valid(self, form):
        if not User.objects.filter(email=form.cleaned_data.get('email')):
            return JsonResponse({"response": 'کاربری با ایمیل وارد شده وجود ندارد'})
        else:
            return render(self.request, self.template_name)


class ChangePasswordView(PasswordChangeView):
    template_name = 'account/change_password.html'
    form_class = ChangePasswordForm

    def form_invalid(self, form):
        for field in form:
            if field.errors:
                err_msg = field.errors
                return JsonResponse({'response': err_msg})
        return super().form_invalid(form)
