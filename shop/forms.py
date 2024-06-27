from django import forms
from .models import Order, OrderItem

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user']

class OrderItemCreateForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity', 'price']