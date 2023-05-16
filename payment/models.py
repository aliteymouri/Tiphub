from django.db import models
from video.models import *


# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='کاربر')
    is_paid = models.BooleanField('پرداخت شده', default=False)
    total_price = models.PositiveIntegerField('قیمت کل', default=0)
    created_at = models.DateTimeField('تاریخ ثبت سفارش در', auto_now_add=True)

    def __str__(self):
        return f"  کاربر {self.user.phone}"

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'
        ordering = ('-created_at',)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='سفارش')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='items', verbose_name='آموزش')
    price = models.PositiveIntegerField('قیمت')

    def __str__(self):
        return self.video.title

    class Meta:
        verbose_name = 'آموزش'
        verbose_name_plural = 'آموزش ها'
