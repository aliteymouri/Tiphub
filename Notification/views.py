from .models import PersonalNotification, GeneralNotification
from django.shortcuts import render
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


# Show All Notification
class Notifications(View):
    template_name = 'notification/notifications.html'

    def get(self, req):
        return render(req, self.template_name)
