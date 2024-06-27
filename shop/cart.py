from django.shortcuts import get_object_or_404
from .models import CartItem, Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product_id, quantity):
        product = Product.objects.get(id=product_id)
        cart_item = self.cart.get(product_id)
        if cart_item:
            cart_item['quantity'] += quantity
        else:
            self.cart[product_id] = {
                'quantity': quantity,
                'price': str(product.price),
            }
        self.save()

    def get_cart_items(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart_items = []
        for product in products:
            cart_items.append({
                'product': product,
                'quantity': self.cart[str(product.id)]['quantity'],
            })
        return cart_items

    def save(self):
        self.session.modified = True

    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['total_price'] = float(item['price']) * item['quantity']
            yield item

    def get_total_price(self):
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session['cart']
        self.save()