from django import template

register = template.Library()

@register.filter
def get_total_price(cart_items):
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return total_price