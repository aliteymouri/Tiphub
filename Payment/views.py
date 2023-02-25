from django.shortcuts import render
from django.views import View


class CartDetailView(View):
    template_name = "payment/buy-basket.html"

    def get(self, req):
        return render(req, self.template_name, {})
