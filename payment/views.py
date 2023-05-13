from django.shortcuts import *
from django.views import *
from video.models import *
from .cart import Cart


class CartDetailView(View):
    template_name = "payment/buy-basket.html"

    def get(self, request):
        return render(request, self.template_name, {'cart': Cart(request)})


class CartAddView(View):
    def post(self, request, pk):
        video = get_object_or_404(Video, id=pk)
        cart = Cart(request)
        cart.add(video)
        return redirect('payment:cart-detail')
