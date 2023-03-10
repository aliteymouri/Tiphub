from django.contrib.auth.forms import ReadOnlyPasswordHashField, PasswordResetForm
from django.contrib.auth.forms import PasswordChangeForm
from captcha.widgets import ReCaptchaV2Checkbox
from captcha.fields import ReCaptchaField
from django.forms import ValidationError
from .models import User
from django import forms


def start_with_09(value):
    if value[:2] != "09" or len(value) < 11:
        raise forms.ValidationError('یک شماره تماس معتبر وارد کنید', code='start_with_09')
    try:
        int(value)
    except:
        raise forms.ValidationError('یک شماره تماس معتبر وارد کنید', code='start_with_09')


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='گذرواژه ',
                               widget=forms.PasswordInput({"placeholder": "گذرواژه", "id": "pass"}))
    confirm_password = forms.CharField(label='تایید گذرواژه ',
                                       widget=forms.PasswordInput(
                                           {"placeholder": "تایید گذرواژه", "id": "confirm_pass"}))

    phone = forms.CharField(
        widget=forms.TextInput({'class': "email-input", "placeholder": "شماره تماس", 'maxlength': 11}),
        validators=[start_with_09]
    )

    class Meta:
        model = User
        fields = ('email', 'fullname', 'phone', 'password')

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValidationError("رمزعبور مشابه نمیباشد")
        elif len(password and confirm_password) < 8:
            raise ValidationError("طول گذرواژه باید حداقل ۸ کاراکتر باشد")
        return confirm_password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text="برای تغییر گذرواژه <a href=\"../password/\">کلیک کنید</a>"
    )

    phone = forms.CharField(
        widget=forms.TextInput({'class': "email-input", "placeholder": "شماره تماس", 'maxlength': 11}),
        validators=[start_with_09]
    )

    class Meta:
        model = User
        fields = (
            'email', 'fullname', 'phone', 'password', 'bio', 'image', 'github', 'linkedin', 'instagram', 'twitter',
            'is_active', 'is_admin', 'is_staff')


class SignInForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput({'class': "email-input", "placeholder": "پست الکترونیک"}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput({'class': "password-input", "placeholder": "گذرواژه", "id": "pass"}),
    )


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput({'class': "email-input", "placeholder": "پست الکترونیک"}),
    )
    fullname = forms.CharField(
        widget=forms.TextInput({'class': "email-input", "placeholder": "نام و نام خانوادگی"}),
    )
    phone = forms.CharField(
        widget=forms.TextInput({'class': "email-input", "placeholder": "شماره تماس", 'maxlength': 11}),
        validators=[start_with_09]
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, error_messages={'required': 'اعتبار سنجی Recaptcha انجام نشد'})


class EditProfileForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.FileInput({'id': 'image'}))

    email = forms.EmailField(
        widget=forms.EmailInput({'class': "email-input", "placeholder": "پست الکترونیک", "id": "email"}),
    )
    fullname = forms.CharField(
        widget=forms.TextInput({'class': "email-input", "placeholder": "نام و نام خانوادگی", "id": "fullname"}),
    )
    phone = forms.CharField(
        widget=forms.TextInput({'class': "email-input", "placeholder": "شماره تماس", 'maxlength': 11, "id": "phone"}),
        validators=[start_with_09]
    )

    github = forms.URLField(required=False,
                            widget=forms.URLInput(
                                {'class': 'email-input', "placeholder": "آدرس گیت هاب", 'id': "github"}))
    linkedin = forms.URLField(required=False,
                              widget=forms.URLInput(
                                  {'class': 'email-input', "placeholder": "آدرس لینکدین", 'id': "linkedin"}))
    instagram = forms.URLField(required=False,
                               widget=forms.URLInput(
                                   {'class': 'email-input', "placeholder": "آدرس اینستاگرام", 'id': "instagram"}))
    twitter = forms.URLField(required=False,
                             widget=forms.URLInput(
                                 {'class': 'email-input', "placeholder": "آدرس توییتر", 'id': "twitter"}))

    bio = forms.CharField(required=False,
                          widget=forms.Textarea(
                              {'class': "form-control", "placeholder": "بیوگرافی", "rows": 3, "id": "bio"})
                          )

    class Meta:
        model = User
        fields = ('image', 'email', 'fullname', 'phone', 'github', 'linkedin', 'instagram', 'twitter', 'bio')


class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput({'class': "email-input", "placeholder": "پست الکترونیک", "id": "email"}),
    )

    def clean_email(self):
        if not User.objects.filter(email=self.cleaned_data.get('email')):
            raise ValidationError("کاربری با ایمیل وارد شده وجود ندارد")
        return self.cleaned_data.get('email')


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput({'placeholder': "گذرواژه فعلی", 'id': "old_password"}))
    new_password1 = forms.CharField(widget=forms.PasswordInput({'placeholder': "گذرواژه جدید", 'id': "new_password1"}))
    new_password2 = forms.CharField(widget=forms.PasswordInput({'placeholder': "تکرار گذرواژه", 'id': "new_password2"}))

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError("گذرواژه فعلی تان اشتباه وارد شد. لطفا دوباره تلاش کنید")
        return old_password