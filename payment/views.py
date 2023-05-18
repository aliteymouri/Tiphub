from django.views.generic import *
from django.shortcuts import *
from .cart import Cart
from .models import *
import requests
import json


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


# Zarinpal payment
MERCHANT = ""  # Your Merchant
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
amount = 11000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
# Important: need to edit for realy server.
CallbackURL = "http://127.0.0.1:8000/payment/verify/"


class SendRequestView(View):
    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        request.session['order_id'] = str(order.id)
        req_data = {
            "merchant_id": MERCHANT,
            "amount": order.total_price,
            "callback_url": CallbackURL,
            "description": description,
            "metadata": {"mobile": request.user.phone, "email": email}
        }
        req_header = {
            "accept": "application/json",
            "content-type": "application/json"
        }
        req = requests.post(
            url=ZP_API_REQUEST,
            data=json.dumps(req_data),
            headers=req_header
        )
        authority = req.json()['data']['authority']
        if len(req.json()['errors']) == 0:
            return redirect(ZP_API_STARTPAY.format(authority=authority))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


class VerifyView(View):
    def get(self, request):
        t_status = request.GET.get('Status')
        t_authority = request.GET['Authority']
        order_id = request.session['order_id']
        order = Order.objects.get(id=int(order_id))
        if request.GET.get('Status') == 'OK':
            req_header = {"accept": "application/json",
                          "content-type": "application/json'"}
            req_data = {
                "merchant_id": MERCHANT,
                "amount": order.total_price,
                "authority": t_authority
            }
            req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
            if len(req.json()['errors']) == 0:
                t_status = req.json()['data']['code']
                if t_status == 100:
                    order.is_paid = True  # transaction success
                    order.save()
                    return HttpResponse('ok')  # you can render a template to show success transaction
                elif t_status == 101:
                    return HttpResponse('Transaction submitted : ' + str(
                        req.json()['data']['message']
                    ))
                else:
                    return HttpResponse('Transaction failed.\nStatus: ' + str(
                        req.json()['data']['message']
                    ))
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
        else:
            return redirect('home:home')
