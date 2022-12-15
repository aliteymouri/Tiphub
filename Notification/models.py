from Account.models import User
from django.db import models
from django.utils import timezone
from persiantools.jdatetime import JalaliDate


class PersonalNotification(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="فرستنده")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="گیرنده", related_name='notifications')
    message = models.TextField("متن اعلان")
    link = models.URLField("لینک", null=True, blank=True)
    created_at = models.DateTimeField("تاریخ ارسال در ", auto_now_add=True)

    def __str__(self):
        return F" اعلان : {self.message}  به کاربر : {self.user.fullname}"

    def get_date(self):
        if self.created_at is not None:
            time = timezone.now() - self.created_at
            s = time.seconds
            if time.days > 30 or time.days < 0:
                return JalaliDate(self.created_at, locale=('fa')).strftime("%c")
            elif time.days >= 1:
                return '{} روز پیش '.format(time.days)
            elif s < 60:
                return '{} ثانیه پیش '.format(s)
            elif s <= 3600:
                return '{} دقیقه پیش '.format(round(s / 60))
            else:
                return '{} ساعت پیش '.format(round(s / 3600))
        else:
            return None

    get_date.short_description = "تاریخ ثبت در"

    class Meta:
        verbose_name = 'اعلان خصوصی'
        verbose_name_plural = 'اعلان های خصوصی'
        ordering = ('-created_at',)


class GeneralNotification(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="فرستنده")
    user = models.ManyToManyField(User, verbose_name="گیرنده", related_name='message')
    message = models.TextField("متن اعلان")
    link = models.URLField("لینک", null=True, blank=True)
    created_at = models.DateTimeField("تاریخ ارسال در ", auto_now_add=True)

    def __str__(self):
        return F" اعلان : {self.message} به کاربران "

    def get_date(self):
        if self.created_at is not None:
            time = timezone.now() - self.created_at
            s = time.seconds
            if time.days > 30 or time.days < 0:
                return JalaliDate(self.created_at, locale=('fa')).strftime("%c")
            elif time.days >= 1:
                return '{} روز پیش '.format(time.days)
            elif s <= 3600:
                return '{} دقیقه پیش '.format(round(s / 60))
            else:
                return '{} ساعت پیش '.format(round(s / 3600))
        else:
            return None

    get_date.short_description = "تاریخ ثبت در"

    class Meta:
        verbose_name = 'اعلان عمومی'
        verbose_name_plural = 'اعلان های عمومی'
        ordering = ('-created_at',)
