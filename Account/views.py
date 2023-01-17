from .forms import SignInForm, SignUpForm, EditProfileForm, ChangePasswordForm
from django.contrib.auth.views import PasswordResetView, PasswordChangeView
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import logout, authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from .mixins import RequiredLoginMixin, AuthenticatedMixin
from django.utils.encoding import force_bytes, force_str
from django.views.generic import CreateView, UpdateView, FormView, TemplateView
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.http import HttpResponse, JsonResponse
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
        form = self.form_class(req.POST, instance=req.user)
        if form.is_valid():
            form.save()
            return JsonResponse({"response":'changed'})
        return render(req, self.template_name, {"form": form})


class ResetPasswordView(PasswordResetView):
    template_name = "account/forgot_password.html"
    email_template_name = "passwords/password_reset_email.html"
    success_url = reverse_lazy('account:password_reset_send')

    def form_valid(self, form):
        if not User.objects.filter(email=form.cleaned_data.get('email')):
            form.add_error("email", "کاربری با ایمیل وارد شده وجود ندارد")
            return super(ResetPasswordView, self).form_invalid(form)
        else:
            return super(ResetPasswordView, self).form_valid(form)


class ChangePasswordView(PasswordChangeView):
    template_name = 'account/change_password.html'
    success_url = reverse_lazy('account:user_panel')
    form_class = ChangePasswordForm


class WhyTipHubView(TemplateView):
    template_name = 'account/why-tiphub.html'


class PrivacyPolicyView(TemplateView):
    template_name = 'account/privacy-policy.html'
