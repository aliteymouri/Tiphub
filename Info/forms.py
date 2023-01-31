from .models import BeTeacher
from django import forms


def start_with_09(value):
    if value[:2] != "09" or len(value) < 11:
        raise forms.ValidationError('یک شماره تماس معتبر وارد کنید', code='start_with_09')


class BeTeacherForm(forms.ModelForm):
    fullname = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "نام و نام خانوادگی"}))
    skill = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "تخصص"}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "پست الکترونیک"}))
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "شماره تماس", 'maxlength': 11,}), validators=[start_with_09])
    resume = forms.FileField()

    class Meta:
        model = BeTeacher
        fields = "__all__"
