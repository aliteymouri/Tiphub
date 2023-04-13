from .models import PersonalNotification, GeneralNotification
from django.views import View


class RemoveNotification(View):
    def get(self, req, pk):
        notification = PersonalNotification.objects.get(id=pk)
        notification.delete()
        pass


class RemoveAdminNotification(View):
    def get(self, req, pk):
        notification = GeneralNotification.objects.get(id=pk)
        notification.user.remove(req.user)
        pass

