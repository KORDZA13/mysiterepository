from .models import Product

def get_cart_items(cart):
    cart_items = []
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        total_price = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': total_price
        })
    return cart_items