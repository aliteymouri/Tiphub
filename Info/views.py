from django.views.generic import TemplateView, FormView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from Info.forms import BeTeacherForm
from Account.models import User


class AboutUsView(TemplateView):
    template_name = "info/about-us.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["members"] = User.objects.filter(is_staff=True)
        return context


class BeTeacherView(FormView):
    template_name = 'info/be-teacher.html'
    success_url = reverse_lazy('home:home')
    form_class = BeTeacherForm

    def form_valid(self, form):
        form.save()
        return redirect('home:home')


class WhyTipHubView(TemplateView):
    template_name = 'info/why-tiphub.html'


class PrivacyPolicyView(TemplateView):
    template_name = 'info/privacy-policy.html'
