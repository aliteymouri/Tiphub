from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from video.models import Video


class CartDetailView(View):
    template_name = "payment/buy-basket.html"

    def get(self, req):
        return render(req, self.template_name, {})


class CartAddView(View):
    def post(self, req, pk):
        video = get_object_or_404(Video, id=pk)
        print(video.title, video.price)
        return redirect('payment:cart-detail')

