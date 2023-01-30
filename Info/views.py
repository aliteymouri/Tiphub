from django.views.generic import TemplateView
from Account.models import User


class AboutUsView(TemplateView):
    template_name = "info/about-us.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["members"] = User.objects.filter(is_staff=True)
        return context
