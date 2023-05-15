from django.db import models

from accounts.models import User
from video.models import Video


# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'
        ordering = ('-created_at',)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return self.order.user