from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Order
from .forms import OrderCreateForm
from django.contrib.auth.decorators import login_required
from .utils import get_cart_items

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            messages.success(request, 'Order created successfully!')
            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderCreateForm()
    return render(request, 'shop/create_order.html', {'form': form})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'shop/order_detail.html', {'order': order})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if the product is available
    if product.quantity > 0:
        cart = request.session.get('cart', {})
        if product_id in cart:
            cart[product_id] += 1
        else:
            cart[product_id] = 1
        request.session['cart'] = cart
        
        # Decrease the product quantity
        product.quantity -= 1
        product.save()
        
        messages.success(request, 'Added item to cart.')
    else:
        messages.error(request, 'This product is out of stock.')
        
    return redirect('view_cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = get_cart_items(cart)
    return render(request, 'shop/cart.html', {'cart_items': cart_items})

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, id=product_id)
    
    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
        
        # Increase the product quantity back
        product.quantity += 1
        product.save()
        
        messages.success(request, 'Removed item from cart.')
    return redirect('view_cart')

def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, id=product_id)
    
    if product_id in cart:
        if cart[product_id] > 1:
            cart[product_id] -= 1
            messages.success(request, 'Decreased item quantity.')
        else:
            del cart[product_id]
            messages.success(request, 'Removed item from cart.')
        request.session['cart'] = cart
        
        # Increase the product quantity
        product.quantity += 1
        product.save()
    
    return redirect('view_cart')

def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, id=product_id)
    
    # Check if the product is available
    if product.quantity > 0:
        if product_id in cart:
            cart[product_id] += 1
        else:
            cart[product_id] = 1
        request.session['cart'] = cart
        
        # Decrease the product quantity
        product.quantity -= 1
        product.save()
        
        messages.success(request, 'Increased item quantity.')
    else:
        messages.error(request, 'This product is out of stock.')
        
    return redirect('view_cart')