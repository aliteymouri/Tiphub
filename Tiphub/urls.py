"""Tiphub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import home
    2. Add a URL to urlpatterns:  path('', home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings
from social_django.models import Association, Nonce, UserSocialAuth
from hitcount.models import BlacklistIP, BlacklistUserAgent, Hit, HitCount

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('home.urls')),
                  path('', include('accounts.urls')),
                  path('', include('video.urls')),
                  path('', include('notification.urls')),
                  path('', include('info.urls')),
                  path('payment/', include('payment.urls')),
                  path('', include('django.contrib.auth.urls')),
                  path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
                  path('', include('social_django.urls', namespace='social')),  # Django_Social
                  path('accounts/', include('allauth.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# 404 page
handler404 = 'home.views.error_404_view'

admin.site.unregister(Association)
admin.site.unregister(Nonce)
admin.site.unregister(UserSocialAuth)

admin.site.unregister(BlacklistIP)
admin.site.unregister(BlacklistUserAgent)
admin.site.unregister(Hit)
admin.site.unregister(HitCount)
