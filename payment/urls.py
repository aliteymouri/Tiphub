from django.urls import path
from . import views

app_name = 'payment'
urlpatterns = [
    path('cart-detail/', views.CartDetailView.as_view(), name='cart-detail'),
    path('add/<int:pk>', views.CartAddView.as_view(), name='cart-add'),
    path('del/<str:pk>', views.CartDeleteView.as_view(), name='cart-del'),
    path('order/creation', views.OrderCreationView.as_view(), name='order-creation'),
    path('order/<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('sendrequest/<int:pk>', views.SendRequestView.as_view(), name='send-request'),
    path('verify-request', views.VerifyView.as_view(), name='verify-request'),
]
