from django.views.generic import TemplateView, FormView, ListView, DetailView
from requests import Response

from info.forms import BeTeacherForm
from django.http import JsonResponse
from django.shortcuts import render
from accounts.models import User
from .serializers import BeTeacherSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class AboutUsView(TemplateView):
    template_name = "info/about-us.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["members"] = User.objects.filter(is_staff=True)
        return context


#
# class BeTeacherView(FormView):
#     template_name = 'info/be-teacher.html'
#     form_class = BeTeacherForm
#
#     def post(self, req, *args):
#         form = self.form_class(req.POST, req.FILES)
#         if form.is_valid():
#             form.save()
#         else:
#             for field in form:
#                 if field.errors:
#                     err_msg = field.errors
#                     return JsonResponse({'errors': err_msg})
#         return render(req, self.template_name)


class BeTeacherView(APIView):

    def get(self, req):
        form = BeTeacherForm
        return render(req, "info/be-teacher.html", {'form': form})

    def post(self, req):
        ser = BeTeacherSerializer(data=req.data)
        if ser.is_valid():
            ser.save()
            return Response({'message': 'ok'})
        return Response(ser.errors)


class TeachersView(ListView):
    queryset = User.objects.filter(is_staff=True)
    template_name = "info/teachers.html"


class TeacherDetailView(DetailView):
    queryset = User.objects.filter(is_staff=True)
    template_name = "info/teacher.html"


class WhyTipHubView(TemplateView):
    template_name = 'info/why-tiphub.html'


class PrivacyPolicyView(TemplateView):
    template_name = 'info/privacy-policy.html'
