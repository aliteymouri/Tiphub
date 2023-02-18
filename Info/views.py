from django.views.generic import TemplateView, FormView, ListView
from Info.forms import BeTeacherForm
from django.http import JsonResponse
from django.shortcuts import render
from Account.models import User


class AboutUsView(TemplateView):
    template_name = "info/about-us.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["members"] = User.objects.filter(is_staff=True)
        return context


class BeTeacherView(FormView):
    template_name = 'info/be-teacher.html'
    form_class = BeTeacherForm

    def post(self, req, *args):
        form = self.form_class(req.POST, req.FILES)
        if form.is_valid():
            form.save()
        else:
            for field in form:
                if field.errors:
                    err_msg = field.errors
                    return JsonResponse({'errors': err_msg})
        return render(req, self.template_name)


class TeachersView(ListView):
    queryset = User.objects.filter(is_staff=True)
    template_name = "info/teachers.html"


class WhyTipHubView(TemplateView):
    template_name = 'info/why-tiphub.html'


class PrivacyPolicyView(TemplateView):
    template_name = 'info/privacy-policy.html'
