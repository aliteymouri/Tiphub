from django.core.validators import FileExtensionValidator
from django.db import models


class BeTeacher(models.Model):
    fullname = models.CharField('نام و نام خانوادگی', max_length=20)
    skill = models.CharField('مهارت', max_length=30, )
    email = models.EmailField('آدرس ایمیل')
    phone_number = models.CharField('شماره تماس', max_length=11, )
    resume = models.FileField('رزومه', upload_to="resume", validators=[
        FileExtensionValidator(['pdf'])])

    class Meta:
        verbose_name = "درخواست تدریس"
        verbose_name_plural = "درخواست‌های تدریس"

    def __str__(self):
        return f"{self.fullname}: {self.skill}"
