from django.shortcuts import *
from django.views import *
from .cart import Cart
from .models import *


class CartDetailView(View):
    template_name = "payment/cart-detail.html"

    def get(self, request):
        return render(request, self.template_name, {'cart': Cart(request)})


class CartAddView(View):
    def post(self, request, pk):
        video = get_object_or_404(Video, id=pk)
        cart = Cart(request)
        cart.add(video)
        return redirect('payment:cart-detail')


class CartDeleteView(View):
    def get(self, request, pk):
        cart = Cart(request)
        cart.delete(pk)
        return redirect('payment:cart-detail')


class OrderCreationView(View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user, total_price=cart.total())
        for item in cart:
            OrderItem.objects.create(order=order, video=item['video'], price=item['price'])
        cart.del_cart()
        return redirect('payment:order-detail', order.id)


class OrderDetailView(View):
    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        return render(request, 'payment/order-detail.html', {'order': order})
