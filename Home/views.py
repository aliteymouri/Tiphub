from django.views.generic.base import TemplateView
from django.shortcuts import render
from Video.models import Video


class HomeView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_videos'] = Video.objects.all().order_by('-updated_on', '-created_at')[:6]
        context['videos'] = Video.objects.all().order_by('views')[:6]
        return context


# def error_404_view(req, exception):
#     return render(req, 'home/404.html')
