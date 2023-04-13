from accounts.forms import start_with_09
from .models import BeTeacher
from django import forms


class BeTeacherForm(forms.ModelForm):
    fullname = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "نام و نام خانوادگی", 'id': 'fullname'}))
    skill = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "تخصص", 'id': 'skill'}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "پست الکترونیک", 'id': 'email'}))
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "شماره تماس", 'maxlength': 11, 'id': 'phone_number'}),
        validators=[start_with_09])
    resume = forms.FileField(widget=forms.FileInput(attrs={'id': 'resume'}))

    class Meta:
        model = BeTeacher
        fields = "__all__"
