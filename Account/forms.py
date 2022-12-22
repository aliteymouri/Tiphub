from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import PasswordChangeForm
from captcha.widgets import ReCaptchaV2Checkbox
from captcha.fields import ReCaptchaField
from django.forms import ValidationError
from .models import User
from django import forms


def start_with_09(value):
    if value[:2] != "09" or len(value) < 11:
        raise forms.ValidationError('یک شماره تماس معتبر وارد کنید', code='start_with_09')


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='گذرواژه ',
                               widget=forms.PasswordInput({"placeholder": "گذرواژه", "id": "pass"}))
    confirm_password = forms.CharField(label='تایید گذرواژه ',
                                       widget=forms.PasswordInput(
                                           {"placeholder": "تایید گذرواژه", "id": "confirm_pass"}))

    class Meta:
        model = User
        fields = ('email', 'fullname', 'phone', 'password')

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValidationError("رمزعبور مشابه نمیباشد")
        elif len(password and confirm_password) < 8:
            raise ValidationError("رمز عبور وارد شده کمتر از 8 کاراکتر میباشد")
        return confirm_password

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) < 11:
            raise ValidationError("یک شماره تماس معتبر وارد کنید")
        return phone

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

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) < 11:
            raise ValidationError("یک شماره تماس معتبر وارد کنید")
        return phone

    class Meta:
        model = User
        fields = ('email', 'fullname', 'phone', 'password', 'bio', 'image', 'is_active', 'is_admin')


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
    bio = forms.CharField(required=False,
                          widget=forms.Textarea(
                              {'class': "form-control", "placeholder": "بیوگرافی", "rows": 3, })
                          )
    image = forms.ImageField(required=False, )

    class Meta:
        model = User
        fields = ('email', 'fullname', 'phone', 'image', 'bio')


# I just customize placeholder and error of PasswordChangeForm

class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'placeholder': "گذرواژه فعلی"})
        self.fields['new_password1'].widget.attrs.update({'placeholder': "گذرواژه جدید"})
        self.fields['new_password2'].widget.attrs.update({'placeholder': "تکرار گذرواژه"})

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError("گذرواژه فعلی تان اشتباه وارد شد. لطفا دوباره تلاش کنید")
        return old_password
