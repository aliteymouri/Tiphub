from video.models import Video

CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, video):
        video_id = video.id
        if video_id not in self.cart:
            self.cart[video_id] = {'id': video.id, 'title': video.title,
                                   'publisher': str(video.publisher_id, ), 'price': str(video.price), 'quantity': 1}
        self.save()

    def __iter__(self):
        cart = self.cart.copy()

        for item in cart.values():
            item['video'] = Video.objects.get(id=int(item['id']))
            item['total'] = int(item['quantity']) * int(item['price'])
            yield item

    def delete(self, pk):
        if pk in self.cart:
            del self.cart[pk]
            self.save()

    def save(self):
        self.session.modified = True
