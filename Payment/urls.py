from django.urls import path
from . import views

app_name = 'payment'
urlpatterns = [
    path('cart-detail/', views.CartDetailView.as_view(), name='cart-detail'),
]
